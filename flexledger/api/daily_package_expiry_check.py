import frappe
from frappe.utils import today,add_days

def check_expiring_packages():
    last_run=frappe.db.get_value("Audit Log",{
        "action":"expiry_date_check",
        "date":today()
    },
    "name")
    if last_run:
        return
    expiry_date=add_days(today(),7)
    packages=frappe.get_all("Package Purchase",filters={
        "status":"Active",
        "expiry_date":["between",[today(),expiry_date]]
    },
    fields=["name"])
    for package in packages:
        frappe.db.set_value("Package Purchase",package.name,"expiry_flag",1)
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name":"Package Purchase",
    "action": "expiry_date_check",
    "user": frappe.session.user,
    "timestamp": frappe.utils.now_datetime(),
    "date": today()
    }).insert(ignore_permissions=True)