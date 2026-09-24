import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	conditions = ["status NOT IN ('Delivered', 'Cancelled')"]

	if filters.device_type:
		conditions.append("device_type = %(device_type)s")

	columns = [
		{"label": "Name", "fieldname": "name", "fieldtype": "Link", "options": "Job Card"},
		{"label": "Customer", "fieldname": "customer_name", "fieldtype": "Data"},
		{"label": "Device Type", "fieldname": "device_type", "fieldtype": "Link", "options": "Device Type"},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data"},
		{"label": "Assigned Technician", "fieldname": "assigned_technician", "fieldtype": "Link", "options": "User"},
		{"label": "Estimated Cost", "fieldname": "estimated_cost", "fieldtype": "Currency"},
		{"label": "Creation", "fieldname": "creation", "fieldtype": "Datetime"},
	]

	data = frappe.db.sql(
		f"""
		SELECT name, customer_name, device_type, status,
		       assigned_technician, estimated_cost, creation
		FROM `tabJob Card`
		WHERE {" AND ".join(conditions)}
		ORDER BY creation DESC
		""",
		filters,
		as_dict=True,
	)

	return columns, data
