import re
import frappe
from frappe.model.document import Document
class JobCard(Document):
    def validate(self):
        if not re.fullmatch(r"\d{10}", self.customer_phone or ""):
            frappe.throw("Phone must have 10 digits.")
        if self.status in ["In Repair", "Ready for Delivery", "Delivered"] and not self.assigned_technician:
            frappe.throw("An assigned technician is required.")
        self.parts_total = 0
        for row in self.parts_used or []:
            row.total_price = (row.quantity or 0) * (row.unit_price or 0)
            self.parts_total += row.total_price
        if not self.labour_charge:
            self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")
        self.final_amount = self.parts_total + (self.labour_charge or 0)
    def before_submit(self):
        if self.status != "Ready for Delivery":
            frappe.throw("Job Card must be Ready for Delivery.")
        for row in self.parts_used or []:
            stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0
            qty = row.quantity or 0
            if stock < qty:
                frappe.throw(f"Insufficient stock for {row.part}. "f"Available: {stock}, Required: {qty}")
    def on_submit(self):
        for row in self.parts_used or []:
            stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0
            frappe.db.set_value(
                "Spare Part", row.part, "stock_qty",
                stock - (row.quantity or 0),
                update_modified=False,
                ignore_permissions=True
            )
        invoice = self.create_service_invoice()
        if invoice:
            self.db_set("service_invoice", invoice.name)
    def create_service_invoice(self):
        existing = frappe.db.get_value("Service Invoice", {"job_card": self.name}, "name")
        if existing:
            return frappe.get_doc("Service Invoice", existing)
        invoice = frappe.new_doc("Service Invoice")
        invoice.job_card = self.name
        invoice.customer_name = self.customer_name
        invoice.labour_charge = self.labour_charge
        invoice.parts_total = self.parts_total
        invoice.total_amount = self.final_amount
        invoice.payment_status = self.payment_status or "Unpaid"
        invoice.insert(ignore_permissions=True)
        return invoice
    def on_cancel(self):
        for row in self.parts_used or []:
            stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0
            frappe.db.set_value(
                "Spare Part", row.part, "stock_qty",
                stock + (row.quantity or 0),
                update_modified=False,
                ignore_permissions=True
            )
        if self.service_invoice and frappe.db.exists("Service Invoice", self.service_invoice):
            invoice = frappe.get_doc("Service Invoice", self.service_invoice)
            if invoice.docstatus == 1:
                invoice.cancel()
        self.db_set("status", "Cancelled")
    def on_trash(self):
        if self.status not in ["Draft", "Cancelled"]:
            frappe.throw("Job Card cannot be deleted.")