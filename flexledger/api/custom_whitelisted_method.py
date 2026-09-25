import frappe
@frappe.whitelist()
def get_member_balance():
    member_id=frappe.form_dict.get("member_id")
    member=frappe.db.get_value("Member",member_id,["name"],as_dict=True)
    if not member:
        frappe.local.response.http_status_code=404
        return{
            "error":"Not found"
        }
    package=frappe.db.get_value("Package Purchase",{
        "member":member_id,
        "status":"Active"
    },
    ["credits_remaining","expiry_date"],as_dict=True) 

    return{
        "member":member_id,
        "credits_remaining":package.credits_remaining if package else 0,
        "expiry_date":package.expiry_date if package else None}