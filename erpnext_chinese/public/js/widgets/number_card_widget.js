import NumberCardWidget from '../../../../../frappe/frappe/public/js/frappe/widgets/number_card_widget.js'

class MyNumberCardWidget extends NumberCardWidget {
	set_title() {
		$(this.title_field).html(`<div class="number-label">${__(this.card_doc.label)}</div>`);
	}
}

frappe.widget.widget_factory.number_card = MyNumberCardWidget