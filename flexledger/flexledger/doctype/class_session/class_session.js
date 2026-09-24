// // Copyright (c) 2026, selciya and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Class Session",{
    setup(frm){
        frm.set_query("trainer",()=>{
            return{
                filters:{
                    status:"Active",
                    specialization:frm.doc.session_type
                }
            }
        })
    },
    refresh(frm){
        if(frm.doc.status==="Draft"){
            frm.dashboard.add_indicator("Draft","orange")
        }
        if(frm.doc.status==="Scheduled"){
            frm.dashboard.add_indicator("Scheduled","blue")
        }
        if(frm.doc.status==="Completed"){
                        frm.dashboard.add_indicator("Completed","green")

        }
        if(frm.doc.status==="Cancelled"){
            frm.dashboard.add_indicator("Cancelled","red")
        }

        const today=frappe.datetime.get_today()
        if(frm.doc.status==="Scheduled" && frm.doc.session_date && frm.doc.session_date<=today)   {
            frm.add_custom_button("Finalize Session",()=>{
                frappe.confirm("Are you sure you want to finalize this session?",()=>{
                    frm.set_value("status","Completed");
                    frm.save();
                })
            })
        }
    
    
        frm.add_custom_button("Cancel Session",()=>{
            const dialog=new frappe.ui.Dialog({
                title:"Cancel Session",
                fields:[{
                    fieldname:"cancellation_reason",
                    label:"Cancellation Reason",
                    fieldtype:"Small Text",
                    reqd:1
                }],
                primary_action_label:"Cancel Session",
                primary_action(values){
                    frm.set_value("status","Cancelled")
                    frm.set_value("cancellation_reason",values.cancellation_reason)
                    dialog.hide()
                    frm.save()
                }

            })
            dialog.show()
        })
    
frm.add_custom_button("Swap Trainer", () => {

    frappe.prompt(
        [
            {
                fieldname: "trainer",
                label: "New Trainer",
                fieldtype: "Link",
                options: "Trainer",
                reqd: 1
            }
        ],

        function (values) {

            frappe.confirm(
                "Are you sure you want to swap the trainer?",
                () => {

                    frappe.call({
                        method: "flexledger.api.swap_trainer.swap_trainer",

                        args: {
                            session: frm.doc.name,
                            trainer: values.trainer
                        },

                        callback: (response) => {

                            if (response.message) {

                                frm.set_value(
                                    "trainer",
                                    values.trainer
                                );

                                frm.trigger("trainer");
                                frm.refresh();
                            }
                        }
                    });
               }
                );
            },

        "Swap Trainer",
        "Continue"
    );
})
    }

});