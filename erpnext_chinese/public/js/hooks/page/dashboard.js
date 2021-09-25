
frappe.pages['dashboard-view'].on_page_show = function(wrapper) {
	const dashboard = frappe.dashboard;
	let title = dashboard.dashboard_name;
	if (dashboard && dashboard.page.title === __('{0} Dashboard', [title])){
		title = __('{0} Dashboard', [__(title)]);
		dashboard.page.set_title(title);
	};
};