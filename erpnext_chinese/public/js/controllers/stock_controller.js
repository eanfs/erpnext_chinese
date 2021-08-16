erpnext.stock.StockController.prototype.show_general_ledger = function() {
    var me = this;
    if(this.frm.doc.docstatus > 0) {
        cur_frm.add_custom_button(__('Accounting Ledger'), function() {
            frappe.route_options = {
                voucher_no: me.frm.doc.name,
                from_date: me.frm.doc.posting_date,
                to_date: moment(me.frm.doc.modified).format('YYYY-MM-DD'),
                company: me.frm.doc.company,
                //group_by: "Group by Voucher (Consolidated)",    //fisher 与系统默认该参数有冲突，帮在此不赋值
                show_cancelled_entries: me.frm.doc.docstatus === 2
            };
            frappe.set_route("query-report", "General Ledger");
        }, __("View"));
    }
}