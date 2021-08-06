import frappe
from frappe.utils import global_search


_search = global_search.search
#fisher 检查用户有权限才返回
@frappe.whitelist()
def search(text, start=0, limit=20, doctype=""):
    ret = []
    limit = int(limit)
    start = int(start)
    require_run_search = True
    result = []
    for i in range(100):
        if not require_run_search: break
        if i == 1:
            start += limit +1
        elif i > 1:
            start += limit
        
        result = _search(text, start, limit, doctype)
        if not result: break
        
        require_run_search = False
        for r in result:
            try:
                doc = frappe.get_doc(r.doctype, r.name)
                if doc.has_permission():
                    ret.append(r)
                    if len(ret) >= limit: break
                else:
                    require_run_search = True
            except frappe.DoesNotExistError:    #due to data inconsistency
                print('not exist',r.doctype, r.name, start)
                frappe.clear_messages()         #hide doc does not exist popup message seen by user
                require_run_search = True 
            
    return ret

global_search.search = search
