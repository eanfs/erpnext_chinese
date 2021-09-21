import frappe
from frappe import _
from frappe.core.doctype.data_import import importer
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