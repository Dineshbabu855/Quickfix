# Copyright (c) 2026, dinesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SparePart(Document):
	def after_insert(self):
		self.name = self.part_code.upper() +"-"+self.name
	def validate(self):
		if self.unit_cost >= self.selling_price:
			frappe.throw("Selling price must greter than Unit Cost")
