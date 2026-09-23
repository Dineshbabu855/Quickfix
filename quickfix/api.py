import frappe
from frappe.query_builder import DocType
from frappe.utils import add_days, now_datetime
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
    try:
        frappe.db.sql("""
            UPDATE `tabJob Card`
            SET assigned_technician = %s
            WHERE assigned_technician = %s
            AND status NOT IN ('Delivered', 'Cancelled')
        """, (to_tech, from_tech))

        frappe.db.commit()

    except Exception:
        frappe.db.rollback()
        frappe.log_error(
            frappe.get_traceback(),
            "QuickFix Technician Transfer Failed"
        )
        raise