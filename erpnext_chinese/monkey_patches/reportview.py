import frappe
from frappe.desk import reportview
from frappe.model.base_document import get_controller

old_get_count = reportview.get_count


@frappe.whitelist()
@frappe.read_only()
def get_count():
    args = reportview.get_form_params()
    if frappe.db.get_value("DocType", filters={"name": args.doctype}, fieldname="is_virtual"):
        controller = get_controller(args.doctype)
        data = len(controller(args.doctype).get_list(args))
    else:
        data = old_get_count()
    return data

reportview.get_count = get_count