import frappe
from frappe.query_builder import DocType
# @frappe.whitelist():
def get_low_balance_members(threshold):
    PP=DocType("Package Purchase")
    result=(
        frappe.qb.from_(PP).select(PP.name,PP.member,PP.credits_remaining,PP.expiry_date).where(PP.credits_remaining<=threshold).where(
            PP.status=="Active").orderby(PP.credits_remaining)
        )
    return result.run(as_dict=True)




    
