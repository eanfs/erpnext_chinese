import frappe
from frappe.model.base_document import BaseDocument
import json

def get_owner_username(self):
    return frappe.db.get_value('User', self.owner, 'full_name')

def get_submit_username(self):
    """变更记录data字段数据格式
    changed:[[其它字段，旧值，新值]
        ['docstatus', 0, 1]
    ]"""
    try:
        if not self.meta.is_submittable:
            return
        filters={'ref_doctype': self.doctype, 'docname': self.name, 'data': ('like', '%docstatus%')}
        version_list = frappe.get_all('Version', filters = filters, fields=['owner','data'], order_by="creation desc")
        for version in version_list:
            data = json.loads(version.data)
            found = [f for f in data.get('changed') if f[0] =='docstatus' and f[-1] ==1]
            if found:
                return frappe.db.get_value('User', version.owner, 'full_name')
    except:
        pass

BaseDocument.get_owner_username = get_owner_username
BaseDocument.get_submit_username = get_submit_username