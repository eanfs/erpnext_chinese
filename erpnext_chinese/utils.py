import frappe


@frappe.whitelist()
def get_user_default():
    return frappe.get_all("User Default", 
        filters = {'user': frappe.session.user},
        fields = ["setting_key", "setting_value"])