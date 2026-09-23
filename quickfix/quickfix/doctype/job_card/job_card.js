frappe.ui.form.on("Job Card", {
    setup(frm) {
        frm.set_query("assigned_technician", () => {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            };
        });
    },
    refresh(frm) {
        if (frm.doc.status === "Pending Diagnosis") {
            frm.dashboard.add_indicator("Pending Diagnosis", "orange");
        } else if (frm.doc.status === "In Repair") {
            frm.dashboard.add_indicator("In Repair", "blue");
        } else if (frm.doc.status === "Ready for Delivery") {
            frm.dashboard.add_indicator("Ready for Delivery", "green");
        } else if (frm.doc.status === "Delivered") {
            frm.dashboard.add_indicator("Delivered", "green");
        } else if (frm.doc.status === "Cancelled") {
            frm.dashboard.add_indicator("Cancelled", "red");
        }
        if (frm.doc.status === "Ready for Delivery" && frm.doc.docstatus === 1) {
            frm.add_custom_button("Mark as Delivered", () => {
                frm.set_value("status", "Delivered");
                frm.save();
            });
        }
    },
    assigned_technician(frm) {
        if (!frm.doc.assigned_technician) {
            return;
        }
        frappe.db.get_value(
            "Technician",
            frm.doc.assigned_technician,
            "specialization"
        ).then(r => {
            if (
                r.message &&
                r.message.specialization &&
                r.message.specialization !== frm.doc.device_type
            ) {
                frappe.msgprint("Technician specialization does not match the device type.");
            }
        });
    }
});
frappe.ui.form.on("Part Usage Entry", {
    quantity(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.model.set_value(
            cdt,
            cdn,
            "total_price",
            (row.quantity || 0) * (row.unit_price || 0)
        );
    }
});