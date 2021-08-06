class MyPermissionEngine  extends frappe.PermissionEngine{
    setup_page() {
		var me = this;
		this.doctype_select
			= this.wrapper.page.add_auto_select(__("Document Type"), this.options.doctypes, 
				function(e) {
					if (e.target.value) {
						frappe.set_route("permission-manager", e.target.value);
					}
				});
		this.role_select
			= this.wrapper.page.add_auto_select(__("Roles"), this.options.roles,
				function() {
					me.refresh();
				});

		this.page.add_inner_button(__('Set User Permissions'), () => {
			return frappe.set_route('List', 'User Permission');
		});
		this.set_from_route();
	}
	// fisher 取设在data-value属性上的实际值而不是显示标签值val()
	get_doctype() {
		let doctype = this.doctype_select.attr("data-value");
		return this.doctype_select.get(0).selectedIndex == 0 ? null : doctype;
	}

	get_role() {
		let role = this.role_select.attr("data-value");
		return this.role_select.get(0).selectedIndex == 0 ? null : role;
	}
}

frappe.PermissionEngine = MyPermissionEngine;