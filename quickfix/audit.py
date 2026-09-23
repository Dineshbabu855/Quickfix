import frappe
from frappe.utils import now


def log_change(doc, method=None):
	if doc.doctype == "Audit Log":
		return

	action = {
		"on_update": "updated",
		"on_submit": "submitted",
		"on_cancel": "cancelled",
	}.get(method, method)
	if not action:
		return

	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doc.doctype,
			"document_name": doc.name,
			"action": action,
			"user": frappe.session.user,
			"timestamp": now(),
		}
	).insert(ignore_permissions=True)
