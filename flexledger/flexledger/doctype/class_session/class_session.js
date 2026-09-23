// Copyright (c) 2026, selciya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Class Session", {
	refresh(frm) {
        
        frm.add_custom_button("Cancel Session",()=>{

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
        frm.set_value({
            "status":"Cancelled"
        })
        frm.refresh_field("status")
        frappe.msgprint("Session Cancelled Successfully")
       
    }
});

d.show();

        })
        

         frm.add_custom_button("Swap Trainer",()=>{
frappe.prompt('Trainer Name',  'Enter Trainer Name', 'Submit').then(doc=>{
     frappe.confirm('Are you sure you want to proceed?',
    () => {
        
    }, () => {
        
    })

})
 
         },


    )
  
frm.set_query('trainer', () => {
    return {
        filters: {
            status: 'Active'
        }
    }
})
if(frm.doc.status){
    const colors={
        Scheduled:"orange",
        Completed:"green",
        Draft:"blue",
        Cancelled:"red"
    }
    frm.dashboard.add_indicator(frm.doc.status,colors[frm.doc.status]||"blue")
}
if(frm.doc.status==="Scheduled" && frm.doc.session_date && frappe.datetime.compare_date(frm.doc.session_date,frappe.datetime.get_today())<=0){
    frm.add_custom_button("Finalize Session",()=>{
        frappe.msgprint("Your session has been finalized")
    })
}


if(frm.doc.status=="Scheduled" && frm.doc.session_date<=today()){
    frm.add_custom_button("Finalize Session",()=>{
      frappe.msgprint("Your session has been finalized")
    })
}
	}
}
);
