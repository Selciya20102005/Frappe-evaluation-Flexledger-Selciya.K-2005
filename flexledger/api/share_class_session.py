import frappe
@frappe.whitelist():
def share_class_session(session_name,user_email):
    session=frappe.get_doc("Class Session",session_name)
    frappe.share.add("Class Session",session_name,user_email,read=1,write=0,share=0)
    return{"sucess":True,
    "message":f"Read access granted to {user_email}"}