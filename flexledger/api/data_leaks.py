import frappe
@frappe.whitelist()
def get_members_unsafe():
    return frappe.get_all("Mmeber",fields=["*"])

@frappe.whitelist()
def get_members_safe():
    user=frappe.session.user
    is_manager="FIT Manager" in frappe.get_roles(user)
    fields=["member_name","join_date","status"]
    if is_manager:
        fields.extend(["phone","email"])
    members=frappe.get_list("Member",fields=fields)
    return members