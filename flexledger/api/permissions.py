import frappe
@frappe.whitelist()
def class_session_permission(user):
    if not user or user=="Guest":
        return "1=0"
    if "FIT Trainer" not in roles:
            return ""
    return f"""
            `tabClass Session`.trainer IN (
                SELECT name
                FROM `tabTrainer`
                WHERE user = {frappe.db.escape(user)}
            )
        """
    
    


