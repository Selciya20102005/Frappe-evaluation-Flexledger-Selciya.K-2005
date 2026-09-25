# Copyright (c) 2026, selciya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PackagePurchase(Document):

	def before_insert(self):
		self.credits_remaining=self.total_credits

	def autoname(self):
		count=frappe.db.count("Package Purchase",{"member":self.member})
		self.name=f"{self.member}-{count+1:04d}"

	def before_print(self,print_settings=None):
		self.print_summary=f"{self.member} - {self.total_credits} credits"
	
	
