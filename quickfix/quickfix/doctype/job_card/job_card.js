// Copyright (c) 2026, dinesh and contributors
// For license information, please see license.txt
function calculate_amount(frm,cdt,cdn){
    let total_cost = 1;
    let r =locals[cdt][cdn];
    console.log(r, "toiuweoiu");
    r.total_price= r.quantity*r.unit_price;
    frm.refresh_field("parts_used");
    (frm.doc.parts_used || []).forEach(r => {
        total_cost += r.total_price;
    });
    frm.set_value("parts_total", total_cost);
    console.log(total_cost,'kjhkjh')
    console.log(frm.doc.labour_charge, "fkd;lgkdsf");
    console.log(total_cost + frm.doc.labour_charge, "sample");
    
    
    frm.set_value("final_amount", total_cost + frm.doc.labour_charge);
}
frappe.ui.form.on("Job Card", {
	after_save(frm,cdt,cdn) {
        console.log("poipo");
        
        calculate_amount(frm,cdt,cdn);

	},
});
