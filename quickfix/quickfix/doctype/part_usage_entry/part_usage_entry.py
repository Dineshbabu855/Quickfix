# Copyright (c) 2026, dinesh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PartUsageEntry(Document):
	def a(self):
		self.total_cost = self.unit_price * self.quantity
