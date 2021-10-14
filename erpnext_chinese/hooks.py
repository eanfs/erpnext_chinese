from . import __version__ as app_version

app_name = "erpnext_chinese"
app_title = "ERPNext Chinese"
app_publisher = "yuzelin"
app_description = "ERPNext中文汉化，简化，优化"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "yuxinyong@163.com"
app_license = "MIT"

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Item-min_pack_qty",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                (
                    'Stock Reconciliation-naming_series-options',
                    'Material Request-naming_series-options',
                    'Production Plan-naming_series-options',
                    'Quality Inspection-naming_series-options',
                    'Pick List-naming_series-options',
                    'Work Order-naming_series-options',
                    'Journal Entry-naming_series-options',
                    'Stock Entry-naming_series-options',
                    'Purchase Receipt-naming_series-options',
                    'Delivery Note-naming_series-options',
                    'Purchase Invoice-naming_series-options',
                    'Sales Invoice-naming_series-options',
                    'Purchase Order-naming_series-options',
                    'Sales Order-naming_series-options',
                    'Contact-last_name-hidden',
                    'User-full_name-hidden',
                    'User-last_name-hidden',
                    'User-middle_name-hidden',
                    'Contact-middle_name-hidden',
                    'Purchase Order-subscription_section-hidden',
                    'Customer-pan-hidden',
                    'Supplier-pan-hidden',
                    'Sales Order-set_warehouse-label',
                    'DocPerm-select-label',
                    'Bank Account-account_subtype-label',
                    'Bank Account-account_type-label',
                    'Bank Account-account_name-label',
                    'Purchase Receipt Item-manufacture_details-label',
                    'Material Request Item-manufacture_details-label',
                    'Supplier Quotation Item-manufacture_details-label',
                    'Purchase Order Item-manufacture_details-label',
                    'Purchase Invoice Item-manufacture_details-label',
                    'Task-weight-label',
                    'Advance Taxes and Charges-rate-label',
                    'Purchase Taxes and Charges-rate-label',
                    'Sales Taxes and Charges-rate-label'
                ),
            ]
        ],
    }
]

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
	"permission-manager": "public/js/hooks/page/permission_manager.js",
    "dashboard-view": "public/js/hooks/page/dashboard.js",
    "print": "public/js/hooks/page/print.js"
}
# include js in doctype views
doctype_js = {
	"User" : "public/js/hooks/doctype/user.js"
}

setup_wizard_requires = "assets/erpnext_chinese/js/setup_wizard.js"
#doctype_list_js = {"Quality Inspection" : "public/js/quality_inspection_list.js"}
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

# doc_events = {
# 	"Purchase Order":{
# 		"before_validate": "erpnext_chinese.api.doc_event.po_validate"
# 	}
# }

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
 	"erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": "erpnext_chinese.localize.localize.get_charts_for_country",
    "erpnext.stock.get_item_details.get_item_details":"erpnext_chinese.utils.new_get_item_details"
}