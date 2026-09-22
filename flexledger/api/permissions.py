import frappe
@frappe.whitelist()
def class_session_permission(user):
    if not user or user=="Guest":
        return "1=0"
    


    return f"`tabClass Session`.trainer={frappe.db.escape(user)}"
