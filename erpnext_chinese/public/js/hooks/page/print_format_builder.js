const MyPrintFormatBuilder = frappe.PrintFormatBuilder.extend({
    setup_section_settings: function() {
		var me = this;
		this.page.main.on("click", ".section-settings", function() {
			var section = $(this).parent().parent();
			var no_of_columns = section.find(".section-column").length;
			var label = section.attr('data-label');

			// new dialog
			var d = new frappe.ui.Dialog({
				title: __("Edit Section"),
				fields: [
					{
						label:__("No of Columns"),
						fieldname:"no_of_columns",
						fieldtype:"Select",
						options: ["1", "2", "3", "4"],
					},
					{
						label:__("Section Heading"),
						fieldname:"label",
						fieldtype:"Data",
						description: __('Will only be shown if section headings are enabled')
					},
					{
						label: __("Remove Section"),
						fieldname: "remove_section",
						fieldtype: "Button",
						click: function() {
							d.hide();
							section.fadeOut(function() {section.remove()});
						},
						input_class: "btn-danger",
						input_css: {
							"margin-top": "20px"
						}
					}
				],
			});

			d.set_input("no_of_columns", no_of_columns + "");
			d.set_input("label", label || "");

			d.set_primary_action(__("Update"), function() {
				// resize number of columns
				me.update_columns_in_section(section, no_of_columns,
					cint(d.get_value("no_of_columns")));

				section.attr('data-label', d.get_value('label') || '');
				section.find('.section-label').html(d.get_value('label') || '');

				d.hide();
			});

			d.show();

			return false;
		});
	},
    setup_field_settings: function() {
		this.page.main.find(".field-settings").on("click", e => {
			const field = $(e.currentTarget).parent();
			// new dialog
			var d = new frappe.ui.Dialog({
				title: __("Set Properties"),
				fields: [
					{
						label: __("Label"),
						fieldname: "label",
						fieldtype: "Data"
					},
					{
						label: __("Align Value"),
						fieldname: "align",
						fieldtype: "Select",
						options: [{'label': __('Left'), 'value': 'left'}, {'label': __('Right'), 'value': 'right'}]
					},
					{
						label: __("Remove Field"),
						fieldtype: "Button",
						click: function() {
							d.hide();
							field.remove();
						},
						input_class: "btn-danger",
						input_css: {
							"margin-top": "10px"
						}
					}
				],
			});

			d.set_value('label', field.attr("data-label"));

			d.set_primary_action(__("Update"), function() {
				field.attr('data-align', d.get_value('align'));
				field.attr('data-label', d.get_value('label'));
				field.find('.field-label').html(d.get_value('label'));
				d.hide();
			});

			// set current value
			if (field.attr('data-align')) {
				d.set_value('align', field.attr('data-align'));
			} else {
				d.set_value('align', 'left');
			}

			d.show();

			return false;
		});
    },
})

$.extend(frappe._messages, {
	"Set Properties": "设置属性",
	"Edit Section": "编辑标题"
})
frappe.templates['print_format_builder_column_selector'] = `
<p class="text-muted">{{ __("Check columns to select, drag to set order.") }} {{ __("Widths can be set in px or %.") }}</p> <p class="help-message alert alert-warning"> {{ __("Some columns might get cut off when printing to PDF. Try to keep number of columns under 10.") }} </p> <div class="row"> <div class="col-sm-6"><h4>{{ __("Column") }}</h4></div> <div class="col-sm-6 text-right"><h4>{{ __("Width") }}</h4></div> </div> <div class="column-selector-list"> {% for (i=0; i < fields.length; i++) { var f = fields[i]; %} {% var selected = in_list(column_names, f.fieldname) %} <div class="row column-selector-row"> <div class="col-sm-6"> <div class="checkbox"> <label> <input type="checkbox" data-fieldname="{{ f.fieldname }}" {{ selected ? "checked" : "" }}> {{ __(f.label) }} </label> </div> </div> <div class="col-sm-6 text-right"> <input class="form-control column-width input-sm text-right" value="{{ (widths[f.fieldname] || "") }}" data-fieldname="{{ f.fieldname }}" style="width: 100px; display: inline" {{ selected ? "" : "disabled" }}> </div> </div> {% } %} </div>
`
frappe.PrintFormatBuilder = MyPrintFormatBuilder