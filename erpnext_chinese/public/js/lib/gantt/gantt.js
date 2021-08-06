let MyGanttView = class MyGanttView extends frappe.views.GanttView {
    get required_libs() {
		return [
			"assets/erpnext_chinese/js/lib/gantt/frappe-gantt.css",
			"assets/erpnext_chinese/js/lib/gantt/frappe-gantt.min.js"
		];
	}
}

frappe.views.GanttView = MyGanttView