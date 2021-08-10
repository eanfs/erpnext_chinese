import frappe, csv, os, json
from frappe import _
from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
	unset_existing_data,build_forest
)
from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts,build_tree_from_json
from erpnext.setup.setup_wizard.operations.taxes_setup import from_detailed_data
from erpnext.accounts.utils import get_coa as old_get_coa
from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import get_charts_for_country as old_get_charts_for_country


def import_coa(company):
	unset_existing_data(company)
	forest = get_chart_data_from_csv()
	create_charts(company, custom_chart=forest)
	set_default_accounts(company)
	set_global_defaults()
	change_field_property()
	setup_tax_template(company)
	setup_tax_rule(company)
	set_item_group_account(company)
	set_warehouse_account(company)

def get_chart_data_from_csv():
	file_path = os.path.join(os.path.dirname(__file__), 'coa_cn.csv')
	data = []
	with open(file_path, 'r') as in_file:
		csv_reader = list(csv.reader(in_file))
		headers = csv_reader[0]
		del csv_reader[0] # delete top row and headers row

		for row in csv_reader:
			if not row[1]:
				row[1] = row[0]
				row[3] = row[2]
			data.append(row)
	forest = build_forest(data)			
	return forest

def set_default_accounts(company):
	file_path = os.path.join(os.path.dirname(__file__), 'default_accounts.csv')
	with open(file_path, 'r') as in_file:
		data = list(csv.reader(in_file))

	company = frappe.get_doc('Company', company)
	company_name = company.name		
	values = {d[0]:frappe.db.get_value("Account",{"company": company_name, "account_name": d[1], "is_group": 0})
				for d in data}
	company.update(values)
	company.save()
	return values

def set_global_defaults():
	frappe.db.set_value('Global Defaults','',{'disable_rounded_total':0,
											'disable_in_words':0}
						)

def change_field_property():
	if bool(frappe.db.get_single_value('System Settings', 'setup_complete')):
		return
	file_path = os.path.join(os.path.dirname(__file__), 'field_property.csv')
	with open(file_path, 'r') as in_file:
		data = list(csv.reader(in_file))
	for (doctype, field_name, prop, value) in data:
		frappe.get_doc({
			'doctype': 'Property Setter',
			'doctype_or_field': 'DocField',
			'doc_type':doctype,
			'field_name': field_name,
			'property':prop,
			'value':value
		}).insert(ignore_permissions=1)

def setup_tax_template(company_name):
	file_path = os.path.join(os.path.dirname(__file__), 'tax_template.json')
	with open(file_path, 'r') as json_file:
		tax_data = json.load(json_file)
	from_detailed_data(company_name, tax_data)

def setup_tax_rule(company_name):
	try:
		abbr = frappe.db.get_value('Company', company_name, 'abbr')
		file_path = os.path.join(os.path.dirname(__file__), 'tax_rule.csv')
		with open(file_path, 'r') as in_file:
			data = list(csv.reader(in_file))
		if data: data = data[1:]
		for (tax_category, tax_type,tax_template) in data:
			template_field_name = 'purchase_tax_template' if tax_type =='Purchase' else 'sales_tax_template'
			tax_rule = frappe.get_doc({
					'doctype':'Tax Rule',
					'tax_category': tax_category,
					'tax_type': tax_type,
					template_field_name: f'{tax_template} - {abbr}',
					'company': company_name})
			tax_rule.insert(ignore_permissions = 1)
	except:
		pass

@frappe.whitelist()
def get_charts_for_country(country, with_standard=False):
	charts = old_get_charts_for_country(country, with_standard)
	if country == 'China':
		charts.insert(0,'中国会计科目表')
	return charts	

def set_warehouse_account(company):
	abbr = frappe.db.get_value('Company', company, 'abbr')
	for wh_detail in [
		[_("Stores"), '1403 - 原材料'],
		[_("Work In Progress"), '141102 - 在用'],
		[_("Finished Goods"), '1405 - 库存商品' ],
		[_("Goods In Transit"), '141101 - 在库']]:
		warehouse_name = f'{wh_detail[0]} - {abbr}'		
		account_name = 	f'{wh_detail[1]} - {abbr}'	
		frappe.db.set_value('Warehouse', warehouse_name, 'account', account_name)

def set_item_group_account(company):
	abbr = frappe.db.get_value('Company', company, 'abbr')
	for wh_detail in [
			[_("Raw Material"), '400101 - 基本生产成本'],
			[_("Sub Assemblies"), '400101 - 基本生产成本'],
			[_("Consumable"), '400101 - 基本生产成本'],
			[_("Services"), '400102 - 辅助生产成本'],
			[_("Products"), '5401 - 主营业务成本']
		]:
		warehouse_name = f'{wh_detail[0]} - {abbr}'		
		account_name = 	f'{wh_detail[1]} - {abbr}'
		item_group_obj = frappe.get_doc('Item Group', wh_detail[0])
		item_group_obj.append('item_group_defaults',{
			'company': company,
			'expense_account': account_name
		})
		item_group_obj.save()

		