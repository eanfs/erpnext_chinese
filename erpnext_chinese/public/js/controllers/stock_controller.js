
let MyStockController = erpnext.stock.StockController.extend({
    show_general_ledger: function() {
        var me = this;
        if(this.frm.doc.docstatus > 0) {
            cur_frm.add_custom_button(__('Accounting Ledger'), function() {
                frappe.route_options = {
                    voucher_no: me.frm.doc.name,
                    from_date: me.frm.doc.posting_date,
                    to_date: moment(me.frm.doc.modified).format('YYYY-MM-DD'),
                    company: me.frm.doc.company,
                    group_by: __("Group by Voucher (Consolidated)"),    //fisher 加了翻译函数
                    show_cancelled_entries: me.frm.doc.docstatus === 2
                };
                frappe.set_route("query-report", "General Ledger");
            }, __("View"));
        }
    }
})

erpnext.stock.StockController = MyStockController;