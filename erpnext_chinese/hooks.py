from . import __version__ as app_version

app_name = "erpnext_chinese"
app_title = "ERPNext Chinese"
app_publisher = "yuzelin"
app_description = "ERPNext中文汉化，简化，优化"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "yuxinyong@163.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_chinese/css/erpnext_chinese.css"
app_include_js = "/assets/js/erpnext_chinese.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_chinese/css/erpnext_chinese.css"
# web_include_js = "/assets/erpnext_chinese/js/erpnext_chinese.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
page_js = {
	"permission-manager": "public/js/hooks/page/permission_manager.js"
}
# include js in doctype views
doctype_js = {
	"User" : "public/js/hooks/doctype/user.js"
}

setup_wizard_requires = "assets/erpnext_chinese/js/setup_wizard.js"
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_chinese.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_chinese.install.before_install"
#after_install = "erpnext_chinese.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_chinese.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }
standard_queries = {
	"DocType": "erpnext_chinese.localize.queries.doctype_role_report_query",
	"Role": "erpnext_chinese.localize.queries.doctype_role_report_query",
	"Report": "erpnext_chinese.localize.queries.doctype_role_report_query"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
        "before_validate": "erpnext_chinese.utils.data.money_in_words_zh_hooks"
#       "on_update": "method",
#       "on_cancel": "method",
#       "on_trash": "method"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_chinese.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_chinese.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_chinese.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_chinese.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_chinese.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_chinese.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
 	"erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": "erpnext_chinese.localize.localize.get_charts_for_country"
}