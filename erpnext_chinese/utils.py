import frappe
import json


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
