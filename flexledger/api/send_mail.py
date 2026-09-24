import frappe
@frappe.whitelist()
def send_low_balance_email(member,package,credits_remaining):
    member_email=frappe.db.get_value("Member",member,"email")
    if not member_email:
        frappe.log_error("Email is missing")
        return
    package_name=frappe.db.get_value("Package Purchase",package,"name")
    if not package_name:
        frappe.log_error("Package has to be entered")
    subject="Low Package Credit Balance"
    message=f"""
    <p>Hello</p>
    <p>Your package {package_name} has a low credit balance</p>"""
    frappe.sendmail(
        recipients=[member_email],
        subject=subject,
        message=message
    )
    