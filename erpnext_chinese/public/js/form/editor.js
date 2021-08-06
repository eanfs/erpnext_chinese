// 用户界面查看角色的权限弹框翻译
const MyRoleEditor = frappe.RoleEditor.extend({
    show_permissions: function(role) {
		// show permissions for a role
		var me = this;
		if(!this.perm_dialog)
			this.make_perm_dialog();
		$(this.perm_dialog.body).empty();
		return frappe.call({
			method: 'frappe.core.doctype.user.user.get_perm_info',
			args: {role: role},
			callback: function(r) {
				var $body = $(me.perm_dialog.body);
				// TODO fix the overflow issue and also display perms like report, import, etc.

				$body.append('<table class="user-perm"><thead><tr>'
					+ '<th style="text-align: left">' + __('Document Type') + '</th>'
					+ '<th>' + __('Level') + '</th>'
					+ '<th>' + __('Read') + '</th>'
					+ '<th>' + __('Write') + '</th>'
					+ '<th>' + __('Create') + '</th>'
					+ '<th>' + __('Delete') + '</th>'
					+ '<th>' + __('Submit') + '</th>'
					+ '<th>' + __('Cancel') + '</th>'
					+ '<th>' + __('Amend') + '</th>'
					+ '<th>' + __('Set User Permissions') + '</th>'
					+ '</tr></thead><tbody></tbody></table>');

				for(var i=0, l=r.message.length; i<l; i++) {
					var perm = r.message[i];

					// if permission -> icon
					for(var key in perm) {
						if (key==='parent') {
							perm[key] = `${__(perm[key])}(${perm[key]})`
                        } else if (key!='permlevel') {
							if(perm[key]) {
								perm[key] = '<i class="fa fa-check"></i>';
							} else {
								perm[key] = '';
							}
						}
					}

					$body.find('tbody').append(repl('<tr>\
						<td style="text-align: left">%(parent)s</td>\
						<td>%(permlevel)s</td>\
						<td>%(read)s</td>\
						<td>%(write)s</td>\
						<td>%(create)s</td>\
						<td>%(delete)s</td>\
						<td>%(submit)s</td>\
						<td>%(cancel)s</td>\
						<td>%(amend)s</td>\
						<td>%(set_user_permissions)s</td>\
						</tr>', perm));
				}
				me.perm_dialog.set_title(__(role));
				me.perm_dialog.show();
			}
		});

	},
})

frappe.RoleEditor = MyRoleEditor