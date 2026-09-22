# Copyright (c) 2026, dinesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		t = frappe.db.get_single_value("QuickFix Settings","default_labour_charge")
		self.labour_charge = t
