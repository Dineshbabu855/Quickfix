# Copyright (c) 2026, dinesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	def autoname(self):
		if not self.invoice_number:
			self.invoice_number = frappe.db.count("Service Invoice") + 1
