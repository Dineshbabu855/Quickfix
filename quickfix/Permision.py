import frappe
def job_card_query(user=None):
    user = user or frappe.session.user
    roles = frappe.get_roles(user)
    if "System Manager" in roles:
        return ""
    if "Manager" in roles:
        return ""
    if "Service Staff" in roles:
        return ""
    if "Technician" not in roles:
        return "1=0"
    technician = frappe.db.get_value(
        "Technician",
        {"user": user},
        "name",
    )
    if not technician:
        return "1=0"
    return frappe.db.escape(
        f"`tabJob Card`.assigned_technician = '{technician}'"
    )