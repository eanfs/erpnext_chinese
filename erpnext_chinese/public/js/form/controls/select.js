const MyControlSelect = frappe.ui.form.ControlSelect.extend({
    set_options: function(value) {
		// reset options, if something new is set
		var options = this.df.options || [];

		if(typeof this.df.options==="string") {
			options = this.df.options.split("\n");
		}

		// nothing changed
		if (JSON.stringify(options) === this.last_options) {
			return;
		}
		this.last_options = JSON.stringify(options);

		if(this.$input) {
			var selected = this.$input.find(":selected").val();
            //fisher 这里加了个字段名参数，以便根据字段名取用自定义翻译，解决一词多义问题
            //console.log('select df=', this.df);
			this.$input.empty().add_options(options || [], this.df && this.df.fieldname);

			if(value===undefined && selected) {
				this.$input.val(selected);
			}
		}
	}
})

//虽然解决了表单及列表显示问题，但解决不了标准报表显示问题，先放一放，将内容直接改回英文
//frappe.ui.form.ControlSelect = MyControlSelect

const custom_translation = {"inspection_type":{"Incoming":"来料检验",
					"Outgoing":"出货检验",
					"In Process":"制程检验"
					}
};
// add <option> list to <select>
(function($) {
	$.fn.add_options = function(options_list, fieldname) {
		// create options
		for(var i=0, j=options_list.length; i<j; i++) {
			var v = options_list[i];
			var value = null;
			var label = null;
			if (!is_null(v)) {
				var is_value_null = is_null(v.value);
				var is_label_null = is_null(v.label);
				var is_disabled = Boolean(v.disabled);

				if (is_value_null && is_label_null) {
					value = v;
                    if (frappe.boot.lang === 'zh' && fieldname && custom_translation[fieldname] && custom_translation[fieldname][value]) {
                        //console.log('custom select option translation single value');
                        label = custom_translation[fieldname][value];
                    } else {
					    label = __(v);
                    }
				} else {
					value = is_value_null ? "" : v.value;
                    //fisher 这里加了个字段名参数，以便根据字段名取用自定义翻译，解决一词多义问题
                    if (frappe.boot.lang === 'zh' && fieldname && custom_translation[fieldname] && custom_translation[fieldname][value]) {
                        //console.log('custom select option translation');
                        label = custom_translation[fieldname][value];
                    } else {
					    label = is_label_null ? __(value) : __(v.label);
                    }
				}
			}

			$('<option>').html(cstr(label))
				.attr('value', value)
				.prop('disabled', is_disabled)
				.appendTo(this);
		}
		// select the first option
		this.selectedIndex = 0;
		$(this).trigger('select-change');
		return $(this);
	};
	$.fn.set_working = function() {
		this.prop('disabled', true);
	};
	$.fn.done_working = function() {
		this.prop('disabled', false);
	};

	let original_val = $.fn.val;
	$.fn.val = function() {
		let result = original_val.apply(this, arguments);
		if (arguments.length > 0) $(this).trigger('select-change');
		return result;
	};
})(jQuery);