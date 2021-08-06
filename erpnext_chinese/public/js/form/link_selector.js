const MyLinkSelector = frappe.ui.form.LinkSelector.extend({
    search: function () {
		var args = {
			txt: this.dialog.fields_dict.txt.get_value(),
			searchfield: "name",
			start: this.start
		};
		var me = this;

		if (this.target.set_custom_query) {
			this.target.set_custom_query(args);
		}

		// load custom query from grid
		if (this.target.is_grid && this.target.fieldinfo[this.fieldname]
			&& this.target.fieldinfo[this.fieldname].get_query) {
			$.extend(args,
				this.target.fieldinfo[this.fieldname].get_query(cur_frm.doc));
		}

		frappe.link_search(this.doctype, args, function (r) {
			var parent = me.dialog.fields_dict.results.$wrapper;
			if (args.start === 0) {
				parent.empty();
			}

			if (r.values.length) {
				$.each(r.values, function (i, v) {
					var row = $(repl('<div class="row link-select-row">\
						<div class="col-xs-4">\
							<b><a href="#">%(name)s</a></b></div>\
						<div class="col-xs-8">\
							<span class="text-muted">%(values)s</span></div>\
						</div>', {
							name: __(v[0]),
							values: v.splice(1).map(v => __(v)).join(", ")
						})).appendTo(parent);

					row.find("a")
						.attr('data-value', v[0])
						.click(function () {
							var value = $(this).attr("data-value");
							var $link = this;
							if (me.target.is_grid) {
								// set in grid
								me.set_in_grid(value);
							} else {
								if (me.target.doctype)
									me.target.parse_validate_and_set_in_model(value);
								else {
									me.target.set_input(value);
									me.target.$input.trigger("change");
								}
								me.dialog.hide();
							}
							return false;
						})
				})
			} else {
				$('<p><br><span class="text-muted">' + __("No Results") + '</span>'
					+ (frappe.model.can_create(me.doctype) ?
						('<br><br><a class="new-doc btn btn-default btn-sm">'
							+ __('Create a new {0}', [__(me.doctype)]) + "</a>") : '')
					+ '</p>').appendTo(parent).find(".new-doc").click(function () {
						frappe.new_doc(me.doctype);
					});
			}

			if (r.values.length < 20) {
				var more_btn = me.dialog.fields_dict.more.$wrapper;
				more_btn.hide();
			}

		}, this.dialog.get_primary_btn());

	},
})

frappe.ui.form.LinkSelector = MyLinkSelector;