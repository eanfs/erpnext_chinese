# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe import _
from frappe.utils import cstr, unique, cint
from six import string_types
from frappe.desk.search import get_std_fields_list
import re


# searches for active employees
@frappe.whitelist()
def doctype_role_report_query(doctype, txt, searchfield=None, start=0, page_len=None, filters=None,reference_doctype=None,ignore_user_permissions=False):
    start = cint(start)
    filter_fields=None

    if isinstance(filters, string_types):
        filters = json.loads(filters)

    if not searchfield:
        searchfield = "name"

    as_dict=False
    meta = frappe.get_meta(doctype)

    if isinstance(filters, dict):
        filters_items = filters.items()
        filters = []
        for f in filters_items:
            if isinstance(f[1], (list, tuple)):
                filters.append([doctype, f[0], f[1][0], f[1][1]])
            else:
                filters.append([doctype, f[0], "=", f[1]])

    if filters==None:
        filters = []
    or_filters = []

    # build from doctype
    if txt:
        search_fields = ["name"]
        if meta.title_field:
            search_fields.append(meta.title_field)

        if meta.search_fields:
            search_fields.extend(meta.get_search_fields())

    if meta.get("fields", {"fieldname":"enabled", "fieldtype":"Check"}):
        filters.append([doctype, "enabled", "=", 1])
    if meta.get("fields", {"fieldname":"disabled", "fieldtype":"Check"}):
        filters.append([doctype, "disabled", "!=", 1])

    # format a list of fields combining search fields and filter fields
    fields = get_std_fields_list(meta, searchfield or "name")
    if filter_fields:
        fields = list(set(fields + json.loads(filter_fields)))
    formatted_fields = ['`tab%s`.`%s`' % (meta.name, f.strip()) for f in fields]

    # find relevance as location of search term from the beginning of string `name`. used for sorting results.
    formatted_fields.append("""locate({_txt}, `tab{doctype}`.`name`) as `_relevance`""".format(
        _txt=frappe.db.escape((txt or "").replace("%", "").replace("@", "")), doctype=doctype))

    # In order_by, `idx` gets second priority, because it stores link count
    from frappe.model.db_query import get_order_by
    order_by_based_on_meta = get_order_by(doctype, meta)
    # 2 is the index of _relevance column
    order_by = "_relevance, {0}, `tab{1}`.idx desc".format(order_by_based_on_meta, doctype)

    ptype = 'select' if frappe.only_has_select_perm(doctype) else 'read'
    ignore_permissions = True if doctype == "DocType" else (cint(ignore_user_permissions) and has_permission(doctype, ptype=ptype))

    page_length = None

    values = frappe.get_list(doctype,
        filters=filters,
        fields=formatted_fields,
        or_filters=or_filters,
        limit_start=start,
        limit_page_length=page_length,
        order_by=order_by,
        ignore_permissions=ignore_permissions,
        reference_doctype=reference_doctype,
        as_list=not as_dict,
        strict=False)

    values = tuple([v for v in list(values) if re.search(re.escape(txt)+".*", (_(v.name) if as_dict else _(v[0])), re.IGNORECASE)
            or re.search(re.escape(txt)+".*", ((v.name) if as_dict else (v[0])), re.IGNORECASE)])

    return [r[:-1] for r in values]   #remove _relevancy
