import ChartWidget from '../../../../../frappe/frappe/public/js/frappe/widgets/chart_widget.js'

class MyChartWidget extends ChartWidget {
	set_chart_title() {
        this.label = __(this.label || this.name);
        super.set_chart_title();
    }
}

frappe.widget.widget_factory.chart = MyChartWidget

frappe.dashboard_utils.render_chart_filters = function(filters, button_class, container, append) {
        console.log('override renderchartfilter');
		filters.forEach(filter => {
			let icon_html = '', filter_class = '';

			if (filter.icon) {
				icon_html = frappe.utils.icon(filter.icon);
			}

			if (filter.class) {
				filter_class = filter.class;
			}
            //fisher 在filter.label前加了翻译函数
			let chart_filter_html =
				`<div class="${button_class} ${filter_class} btn-group dropdown pull-right">
					<a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						<button class="btn btn-secondary btn-xs">
			 				${icon_html}
							<span class="filter-label">${__(filter.label)}</span>
							${frappe.utils.icon('select', 'xs')}
						</button>
				</a>`;
			let options_html;
            //fisher 以下两个Option前加了翻译函数，使用selected_item 原值取代已翻译的标签    
			if (filter.fieldnames) {
				options_html = filter.options.map((option, i) =>
					`<li>
						<a class="dropdown-item" data-fieldname="${filter.fieldnames[i]}" selected_item="${option}">${__(option)}</a>
					</li>`).join('');
			} else {
				options_html = filter.options.map( option => `<li><a class="dropdown-item" selected_item="${option}">${__(option)}</a></li>`).join('');
			}

			let dropdown_html = chart_filter_html + `<ul class="dropdown-menu">${options_html}</ul></div>`;
			let $chart_filter = $(dropdown_html);

			if (append) {
				$chart_filter.prependTo(container);
			} else $chart_filter.appendTo(container);

			$chart_filter.find('.dropdown-menu').on('click', 'li a', (e) => {
				let $el = $(e.currentTarget);
				let fieldname;
				if ($el.attr('data-fieldname')) {
					fieldname = $el.attr('data-fieldname');
				}
				//fisher 使用selected_item 原值取代已翻译的标签,下一行的selected_text也加上翻译函数 	
				let selected_item = $el.attr('selected_item');	// $el.text();
				$el.parents(`.${button_class}`).find('.filter-label').text(__(selected_item));
				filter.action(selected_item, fieldname);
			});
		});

	}
