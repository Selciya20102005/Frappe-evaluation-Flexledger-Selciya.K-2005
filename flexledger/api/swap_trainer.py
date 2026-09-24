import frappe
@frappe.whitelist()
def swap_trainer(session,trainer):
    class_session=frappe.get_doc("Class Session",session)
    class_session.trainer=trainer
    class_session.save()
    return({"trainer":trainer})