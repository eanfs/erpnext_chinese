import frappe
from erpnext.setup.doctype.company.company import Company
from erpnext_chinese.localize.localize import import_coa

old_create_default_accounts = Company.create_default_accounts

def create_default_accounts(self):
    if self.chart_of_accounts == '中国会计科目表':
        self.create_default_warehouses()
        frappe.local.flags.ignore_root_company_validation = True
        frappe.local.flags.ignore_chart_of_accounts = True      #bypass system to set default accounts
        import_coa(self.name)
        
    else:
        old_create_default_accounts()

Company.create_default_accounts = create_default_accounts