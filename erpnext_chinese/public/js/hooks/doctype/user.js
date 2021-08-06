// 用户界面允许模块翻译
const MyModuleEditor = frappe.ModuleEditor.extend({
    make: function() {
		var me = this;
		this.frm.doc.__onload.all_modules.forEach(function(m) {
			$(repl('<div class="col-sm-6"><div class="checkbox">\
				<label><input type="checkbox" class="block-module-check" data-module="%(module)s">\
				%(module_tran)s</label></div></div>', {module: m,module_tran: __(m)})).appendTo(me.wrapper);
		});
		this.bind();
	},
})

frappe.ModuleEditor = MyModuleEditor