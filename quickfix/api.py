import frappe
from frappe.query_builder import DocType
from frappe.utils import add_days, now_datetime
from frappe.utils import today
def get_overdue_jobs():
    JC =DocType("Job Card")
    cutoff = add_days(now_datetime(), -7)
    return (
        frappe.qb.from_(DocType("Job Card"))
        .select(
            JC.name,
            JC.customer_name,
            JC.assigned_technician,
            JC.creation
        )
        .where(
            (JC.status.isin(["Pending Diagnosis", "In Repair"]))
            & (JC.creation < cutoff)
        )
        .orderby(JC.creation)
        .run(as_dict=True)
    )
def transfer_job(from_tech, to_tech):
    frappe.db.sql("""
        UPDATE `tabJob Card`
        SET assigned_technician = %s
        WHERE assigned_technician = %s
        AND status NOT IN ('Delivered', 'Cancelled')
    """, (to_tech, from_tech))
    frappe.db.commit()
def low_stack():
    s = frappe.get_single_value("QuickFix Settings","low_stock_alert_enabled")
    doc = frappe.db.get_value("Audit Log",{"action": "low_stock_check", "timestamp": today()},"name")
    if not s or not doc ==None :
        return 
    low =  frappe.get_all("Spare Part",filters={"is_active": 1},fields=["name", "stock_qty", "reorder_level"])
    for l in low:
        if l.stock_qty <= l.reorder_level:
            print(l)
            d = frappe.new_doc("Audit Log")
            d.action = "low_stock_check"
            d.timestamp = frappe.utils.now()
            d.date = today()
            d.doctype_name = "Spare Part"
            d.document_name = l.name
            d.user = frappe.session.user
            d.insert(ignore_permissions=True)
            frappe.db.commit()
            
