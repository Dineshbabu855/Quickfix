import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):

    def autoname(self):
        self.part_code = (self.part_code or "").strip().upper()
        if not self.part_code:
            frappe.throw("Part Code is required.")
        self.name = make_autoname(f"{self.part_code}-PART-.YYYY.-.####")

    def validate(self):
        if self.selling_price <= self.unit_cost:
            frappe.throw("Selling Price must be greter than Unit Cost")