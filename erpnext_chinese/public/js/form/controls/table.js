const MyControlTable = frappe.ui.form.ControlTable.extend({
	make: function() {
		this._super();

		this.$wrapper.on('paste', ':text', e => {
			const table_field = this.df.fieldname;
			const grid = this.grid;
			const grid_pagination = grid.grid_pagination;
			const grid_rows = grid.grid_rows;
			const doctype = grid.doctype;
			const row_docname = $(e.target).closest('.grid-row').data('name');
			const in_grid_form = $(e.target).closest('.form-in-grid').length;

			let pasted_data = frappe.utils.get_clipboard_data(e);

			if (!pasted_data || in_grid_form) return;

			let data = frappe.utils.csv_to_array(pasted_data, '\t');

			if (data.length === 1 && data[0].length === 1) return;

			let fieldnames = [];
			// for raw data with column header
			if (this.get_field(data[0][0])) {
				data[0].forEach(column => {
					fieldnames.push(this.get_field(column));
				});
				data.shift();
			} else {
				// no column header, map to the existing visible columns
				const visible_columns = grid_rows[0].get_visible_columns();
				let target_column_matched = false;
				visible_columns.forEach(column => {
					// consider all columns after the target column.
					if (target_column_matched || column.fieldname === $(e.target).data('fieldname')) {
						fieldnames.push(column.fieldname);
						target_column_matched = true;
					}
				});
			}

			let row_idx = locals[doctype][row_docname].idx;
			let data_length = data.length;
			data.forEach((row, i) => {
				setTimeout(() => {
					let blank_row = !row.filter(Boolean).length;
					if (!blank_row) {
						if (row_idx > this.frm.doc[table_field].length) {
							this.grid.add_new_row();
						}

						if (row_idx > 1 && (row_idx - 1) % grid_pagination.page_length === 0) {
							grid_pagination.go_to_page(grid_pagination.page_index + 1);
						}

						const row_name = grid_rows[row_idx - 1].doc.name;
						row.forEach((value, data_index) => {
							if (fieldnames[data_index]) {
                                //fisher 保存文本编辑器字段的回车换行
                                if (value) {
                                    const fieldtype = frappe.meta.get_field(doctype,fieldnames[data_index]).fieldtype;
						            if (fieldtype && fieldtype ==='Text Editor') {
                                        console.log('text editor field line break replaced');
                                        value = value.replace(/[\n\r]/g,'<br>');
                                    }    
                                 };
								frappe.model.set_value(doctype, row_name, fieldnames[data_index], value);
							}
						});
						row_idx++;
					}
                    //fisher 移到外面来，复制的最后空行不会导致进度条走不完
                    if (data_length >= 10) {
                        let progress = i + 1;
                        frappe.show_progress(__('Processing'), progress, data_length, null, true);
                    }
				}, 0);
			});
			return false; // Prevent the default handler from running.
		});
	}
});

frappe.ui.form.ControlTable = MyControlTable;