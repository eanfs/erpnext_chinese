# import frappe
# from frappe import _
# from erpnext.controllers.accounts_controller import AccountsController, get_advance_journal_entries


# def get_advance_payment_entries(party_type, party, party_account, order_doctype,
# 		order_list=None, include_unallocated=True, against_all_orders=False, limit=None):
# 	party_account_field = "paid_from" if party_type == "Customer" else "paid_to"
# 	currency_field = "paid_from_account_currency" if party_type == "Customer" else "paid_to_account_currency"
# 	payment_type = "Receive" if party_type == "Customer" else "Pay"
# 	exchange_rate_field = "source_exchange_rate" if payment_type == "Receive" else "target_exchange_rate"

# 	payment_entries_against_order, unallocated_payment_entries = [], []
# 	limit_cond = "limit %s" % limit if limit else ""

# 	if order_list or against_all_orders:
# 		if order_list:
# 			reference_condition = " and t2.reference_name in ({0})" \
# 				.format(', '.join(['%s'] * len(order_list)))
# 		else:
# 			reference_condition = ""
# 			order_list = []

# 		payment_entries_against_order = frappe.db.sql("""
# 			select
# 				"Payment Entry" as reference_type, t1.name as reference_name,
# 				t1.remarks, t2.allocated_amount as amount, t2.name as reference_row,
# 				t2.reference_name as against_order, t1.posting_date,
# 				t1.{0} as currency, t1.{3} as exchange_rate
# 			from `tabPayment Entry` t1, `tabPayment Entry Reference` t2
# 			where
# 				t1.name = t2.parent and t1.payment_type = %s
# 				and t1.party_type = %s and t1.party = %s and t1.docstatus = 1
# 				and t2.reference_doctype = %s {1}
# 			order by t1.posting_date {2}
# 		""".format(currency_field, reference_condition, limit_cond, exchange_rate_field),
# 													  [payment_type, party_type, party,
# 													   order_doctype] + order_list, as_dict=1)

# 	if include_unallocated:
# 		unallocated_payment_entries = frappe.db.sql("""
# 				select "Payment Entry" as reference_type, name as reference_name,
# 				remarks, unallocated_amount as amount, {2} as exchange_rate
# 				from `tabPayment Entry`
# 				where
# 					{0} = %s and party_type = %s and party = %s and payment_type = %s
# 					and docstatus = 1 and unallocated_amount > 0
# 				order by posting_date {1}
# 			""".format(party_account_field, limit_cond, exchange_rate_field),
# 			(party_account, party_type, party, payment_type), as_dict=1)

# 	return list(payment_entries_against_order) + list(unallocated_payment_entries)

# def get_advance_entries(self, include_unallocated=True):
#     if self.doctype == "Sales Invoice":
#         party_account = self.debit_to
#         party_type = "Customer"
#         party = self.customer
#         amount_field = "credit_in_account_currency"
#         order_field = "sales_order"
#         order_doctype = "Sales Order"
#     else:
#         party_account = self.credit_to
#         party_type = "Supplier"
#         party = self.supplier
#         amount_field = "debit_in_account_currency"
#         order_field = "purchase_order"
#         order_doctype = "Purchase Order"

#     order_list = list(set(d.get(order_field)
#         for d in self.get("items") if d.get(order_field)))

#     journal_entries = get_advance_journal_entries(party_type, party, party_account,
#         amount_field, order_doctype, order_list, include_unallocated)

#     payment_entries = get_advance_payment_entries(party_type, party, party_account,
#         order_doctype, order_list, include_unallocated, against_all_orders=True)

#     res = journal_entries + payment_entries

#     return res

# AccountsController.get_advance_entries = get_advance_entries   