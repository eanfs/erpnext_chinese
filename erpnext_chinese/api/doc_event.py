import frappe
from frappe import _
import math

def po_validate(doc, method):
    #抽取物料号
    if not frappe.db.has_column('Item','min_pack_qty'):return
    item_code_list = [item.item_code for item in doc.items]
    qty_list = frappe.get_all("Item", filters = {'item_code':('in', item_code_list)},
        fields =['item_code','purchase_uom','min_pack_qty'])
    #转换成字典
    qty_dict = {(item.item_code, item.purchase_uom):item.min_pack_qty for item in qty_list}
    for item in doc.items:
        min_pack_qty = qty_dict.get((item.item_code, item.uom), 0)
        if min_pack_qty:
            Quotient = item.qty / min_pack_qty
            rounded_quotient = math.floor(Quotient)
            if Quotient > rounded_quotient:
                old_qty = item.qty
                item.qty = (rounded_quotient + 1) * min_pack_qty
                item.stock_qty = item.qty * item.conversion_factor
                frappe.msgprint(_('Item {0} Qty {1} changed to {2} due to min pack qty {3}'
                    .format(item.item_code, old_qty,item.qty, min_pack_qty)))