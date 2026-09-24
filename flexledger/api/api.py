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

# @frappe.whitelist()
def transfer_package(package_name,new_member):
    try:
        frappe.db.sql("""
        UPDATE  tabPackage Purchase` SET member=%s WHERE name=%s""",(new_member,package_name))
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(),"Package Transfer Failed")
        raise




    
