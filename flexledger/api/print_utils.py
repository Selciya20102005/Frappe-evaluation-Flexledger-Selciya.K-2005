import frappe
def get_studio_name():
    s= frappe.get_single("Studio Settings")
    return s.studio_name

def format_value(value,fieldtype):
    return frappe.format_value(value,{"fieldtype":fieldtype})
