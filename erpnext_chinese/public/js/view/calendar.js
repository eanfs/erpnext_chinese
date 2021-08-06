var MyCalendar = frappe.views.Calendar.extend({
    setup_options: function(defaults) {
        this._super(defaults);
        if (this.cal_options.locale == 'zh') {
            this.cal_options.locale = 'zh-cn'
        }
    }
})

frappe.views.Calendar = MyCalendar