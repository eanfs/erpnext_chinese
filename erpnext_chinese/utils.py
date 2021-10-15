import frappe
import json
from erpnext.stock.get_item_details import get_item_details
from six import string_types


@frappe.whitelist()
def get_user_default():
    return frappe.get_all("User Default", 
        filters = {'user': frappe.session.user},
        fields = ["setting_key", "setting_value"])

@frappe.whitelist()
def get_print_format(doc):
    if not frappe.db.has_column('Print Format', 'condition_for_default'):
        return

    if isinstance(doc, str):
        doc = json.loads(doc)
    doc = frappe.get_doc(doc)
    print_format_list =  frappe.get_all('Print Format', 
                                        filters = {'doc_type': doc.doctype,
                                                   'disabled': 0},
                                        fields = ['name', 'condition_for_default'],
                                        order_by = 'priority', as_list = 1)

    for (print_format, condition) in print_format_list:
        if condition and frappe.safe_eval(condition, None, dict(doc=doc, get_roles = frappe.get_roles)):
            return print_format

@frappe.whitelist()
def new_get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
    """fisher 修复旧物料切换到默认交易(采购、销售)单位与基本单位不同的新物料，单位转换率不自动刷新的问题"""
    if isinstance(args, string_types):
        args = json.loads(args)
    
    args.pop('conversion_factor', None)
    return get_item_details(args, doc=doc, for_validate=for_validate, overwrite_warehouse=overwrite_warehouse)
