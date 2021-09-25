import frappe
from frappe import _
from frappe.core.doctype.data_import import importer
from frappe.core.doctype.data_import.importer import ImportFile,INVALID_VALUES,MAX_ROWS_IN_PREVIEW
from frappe.core.doctype.data_import.importer import build_fields_dict_for_column_matching as old_build_fields_dict_for_column_matching
from frappe.core.doctype.data_import.exporter import Exporter
from frappe.core.doctype import data_import


def new_build_fields_dict_for_column_matching(parent_doctype):
    """支持中文字段标签"""
    out = old_build_fields_dict_for_column_matching(parent_doctype)

    if frappe.translate.get_user_lang != 'en':
        to_be_trans = {label: field for (label, field) in out.items() if '.' not in label}
        for label, field in to_be_trans.items():
            if ' (' in label:
                child_field, child_table = label.split(' (', 1)
                chield_table = child_table[:-1]
                trans_label = f"{_(child_field)} ({_(chield_table)})"
            else:
                trans_label = _(label)
            if trans_label != label:
                out[trans_label] = field
    return out

importer.build_fields_dict_for_column_matching = new_build_fields_dict_for_column_matching

def new_add_header(self):
    header = []
    for df in self.fields:
        is_parent = not df.is_child_table_field
        if is_parent:
            label = _(df.label)
        else:
            label = "{0} ({1})".format(_(df.label), _(df.child_table_df.label))

        if label in header:
            # this label is already in the header,
            # which means two fields with the same label
            # add the fieldname to avoid clash
            if is_parent:
                label = "{0}".format(df.fieldname)
            else:
                label = "{0}.{1}".format(df.child_table_df.fieldname, df.fieldname)
        header.append(label)

    self.csv_array.append(header)

Exporter.add_header = new_add_header

def parse_next_row_for_import(self, data):
    """
    Parses rows that make up a doc. A doc maybe built from a single row or multiple rows.
    Returns the doc, rows, and data without the rows.
    """
    doctypes = self.header.doctypes

    # first row is included by default
    first_row = data[0]
    rows = [first_row]

    # if there are child doctypes, find the subsequent rows
    if len(doctypes) > 1:
        # subsequent rows that have blank values in parent columns
        # are considered as child rows
        parent_column_indexes = self.header.get_column_indexes(self.doctype)
        parent_row_values = first_row.get_values(parent_column_indexes)

        data_without_first_row = data[1:]
        for row in data_without_first_row:
            row_values = row.get_values(parent_column_indexes)
            # if the row is blank, it's a child row doc fisher 下一行与上一行主单据内容相同时也作为同一个单据
            if all([v in INVALID_VALUES for v in row_values]) or row_values == parent_row_values:
                rows.append(row)
                continue
            # if we encounter a row which has values in parent columns,
            # then it is the next doc
            break

    parent_doc = None
    for row in rows:
        for doctype, table_df in doctypes:
            if doctype == self.doctype and not parent_doc:
                parent_doc = row.parse_doc(doctype)

            if doctype != self.doctype and table_df:
                child_doc = row.parse_doc(doctype, parent_doc, table_df)
                if child_doc is None:
                    continue
                parent_doc[table_df.fieldname] = parent_doc.get(table_df.fieldname, [])
                parent_doc[table_df.fieldname].append(child_doc)

    doc = parent_doc

    return doc, rows, data[len(rows) :]

ImportFile.parse_next_row_for_import = parse_next_row_for_import


def get_data_for_import_preview(self):
    """Adds a serial number column as the first column"""
    #翻译第一个序号字段
    columns = [frappe._dict({"header_title": _("Row #"), "skip_import": True})]
    columns += [col.as_dict() for col in self.columns]
    for col in columns:
        # only pick useful fields in docfields to minimise the payload
        if col.df:
            col.df = {
                "fieldtype": col.df.fieldtype,
                "fieldname": col.df.fieldname,
                "label": col.df.label,
                "options": col.df.options,
                "parent": col.df.parent,
                "reqd": col.df.reqd,
                "default": col.df.default,
                "read_only": col.df.read_only,
            }

    data = [[row.row_number] + row.as_list() for row in self.data]

    warnings = self.get_warnings()

    out = frappe._dict()
    out.data = data
    out.columns = columns
    out.warnings = warnings
    total_number_of_rows = len(out.data)
    if total_number_of_rows > MAX_ROWS_IN_PREVIEW:
        out.data = out.data[:MAX_ROWS_IN_PREVIEW]
        out.max_rows_exceeded = True
        out.max_rows_in_preview = MAX_ROWS_IN_PREVIEW
        out.total_number_of_rows = total_number_of_rows
    return out

ImportFile.get_data_for_import_preview = get_data_for_import_preview