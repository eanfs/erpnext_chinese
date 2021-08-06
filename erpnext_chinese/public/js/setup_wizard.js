frappe.setup.on("after_load", function () {
	//frappe.setup.data.default_language = "简体中文";
    frappe.wizard.values.language = "简体中文";
    frappe.wizard.values.country = "China";
    frappe.wizard.values.timezone = "Asia/Chongqing";
    frappe.wizard.values.currency = "CNY";
});
