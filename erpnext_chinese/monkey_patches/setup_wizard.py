import frappe
from frappe import _
from erpnext_chinese.localize.localize import get_chart_data_from_csv
import erpnext

@frappe.whitelist()
def get_coa(doctype, parent, is_root = False, chart=None):
    from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import build_tree_from_json
    # add chart to flags to retrieve when called from expand all function
    chart = chart if chart else frappe.flags.chart
    frappe.flags.chart = chart
    parent = None if parent==_('All Accounts') else parent
    if chart == '中国会计科目表':
        forest = get_chart_data_from_csv()
        accounts = build_tree_from_json('dummy',chart_data=forest)
    else:    
        accounts = build_tree_from_json(chart) # returns alist of dict in a tree render-able form

    # filter out to show data for the selected node only
    accounts = [d for d in accounts if d['parent_account']==parent]        

    return accounts

erpnext.accounts.utils.get_coa = get_coa