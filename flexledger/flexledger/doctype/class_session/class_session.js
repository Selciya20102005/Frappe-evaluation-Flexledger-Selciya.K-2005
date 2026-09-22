// Copyright (c) 2026, selciya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Class Session", {
	refresh(frm) {
        add_custom_button("Cancel Session",()=>{
//             let dialog=new frappe.ui.Dialog({
//                 title:"Cancellation Reason",
//                 field:{
// fieldname:"cancellation_reason",
// label:"Cancellation Reason",
// fieldtype:"Small Text",
// redq:1
//                 }
                

//             }
        
//     )
//     dialog.show()
let d = new frappe.ui.Dialog({
    title: 'Cancellation Reason',
    fields: [
        {
            label: 'Reason',
            fieldname: 'reason',
            fieldtype: 'Small Text'
        }
        
    ],
    size: 'small', // small, large, extra-large 
    primary_action_label: 'Send',
    primary_action(values) {
        frappe.db.set_value("Class Session",frm.doc.name,"status","Cancelled")
        
    }
});

d.show();

        })

	}
});
