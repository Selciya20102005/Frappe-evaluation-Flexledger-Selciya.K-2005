# Copyright (c) 2026, selciya and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Trainer(Document):
	def rename_trainer(old,new):
		frappe.rename_doc("Trainer",old,new,merge=False)
	
