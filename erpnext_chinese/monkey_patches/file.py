import frappe
from frappe.core.doctype.file import file


"""file_name后的Home及Attachement不调用翻译函数，因为后续上传文件时根目录参数是没翻译的"""
def make_home_folder():
	home = frappe.get_doc({
		"doctype": "File",
		"is_folder": 1,
		"is_home_folder": 1,
		"file_name": "Home"
	}).insert()

	frappe.get_doc({
		"doctype": "File",
		"folder": home.name,
		"is_folder": 1,
		"is_attachments_folder": 1,
		"file_name": "Attachments"
	}).insert()

file.make_home_folder = make_home_folder