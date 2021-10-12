class MyPrintPreview  extends frappe.ui.form.PrintView{
    show(frm) {
		this.frm = frm;
		this.set_title();
		this.set_breadcrumbs();
        //fisher 之前按单据类型默认打印格式，此外需重新左边栏以实现按单据默认
        this.page && this.page.sidebar && this.page.sidebar.empty();
        this.setup_sidebar();

		this.setup_customize_dialog();

		let tasks = [
            this.refresh_print_options,
			this.set_default_print_language,
			this.set_letterhead_options,
			this.preview,
		].map((fn) => fn.bind(this));
        
		this.setup_additional_settings();
		return frappe.run_serially(tasks);
	}
    
    selected_format() {
        let current_print_format = this.print_sel.val();
        if (current_print_format){
            return current_print_format
        }
        else {
            frappe.call({
                method: 'erpnext_chinese.utils.get_print_format',
                args: {doc: this.frm.doc}
            }).then((r) =>{
                //console.log('r.message=', r.message);
                this.print_sel.val(r.message || this.frm.meta.default_print_format || 'Standard');
                this.refresh_print_format();
            })
        }
    }
}

frappe.ui.form.PrintView = MyPrintPreview;