import frappe
def after_install():
    session_types=[("1:1 Personal Training",2),("Group HIIT",1),("Yoga Flow",1)]
    for session_type,credits_required in session_types:
        if not frappe.db.exists("Session Type",session_type):
            doc=frappe.new_doc("Session Type")
            doc.session_type_name=session_type
            doc.credits_required=credits_required
            doc.insert(ignore_permissions=True)

    if not frappe.db.exists("Studio Settings","Flexledger Studio"):
        s=frappe.get_single("Studio Settings")
        s.no_show_forfeits_credit=0
        s.low_balance_alert_threshold=10
        s.studio_name="Flexledger Studio"
        s.manager_email="selciya@gmail.com"
        s.save(ignore_permissions=True)
    frappe.msgprint("Flexledger installed successfully")