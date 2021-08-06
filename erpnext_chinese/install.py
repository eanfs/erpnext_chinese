# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals

import frappe
import os


def after_install():
    """加载到翻译表里以便程序直接加载到前端网页，翻译那些框架程序中未获取待翻译文本而未被翻译的内容"""
    app = 'erpnext_chinese'
    lang = 'zh'
    path = os.path.join(frappe.get_pymodule_path('erpnext_chinese'), "translations", f'{lang}_global.csv')
    data =  frappe.translate.get_translation_dict_from_file(path, lang, app)
    source_text = list(data.keys())
    frappe.db.delete('Translation', conditions={'language':lang,'source_text':('in', source_text)})
    for k, v in data.items():
        frappe.get_doc({'doctype':'Translation','language':lang, 'source_text': k, 'translated_text': v}).insert()	
    frappe.db.commit()
