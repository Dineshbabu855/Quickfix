import frappe
def create():
    for d in ["SmartPhone","Laptop","Tablet"]:
        if not frappe.db.exists("Device Type",d):
            doc = frappe.new_doc("Device Type")
            doc.device_type = d
            doc.insert(ignore_permissions=True)
    if not frappe.db.exists("QuickFix Settings"):
        doc = frappe.new_doc("QuickFix Settings")
        doc.shop_name = "QuickFix"
        doc.manager_email = "manager@quickfix.com"
        doc.insert(ignore_permissions=True)
    frappe.msgprint("QuickFix Setup Completed")