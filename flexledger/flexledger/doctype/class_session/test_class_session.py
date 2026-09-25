# Copyright (c) 2026, selciya and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestClassSession(IntegrationTestCase):
	def deduct_attendee_credits(self,attendee,studio_settings):
			credits_charged=attendee.credits_charged or 0
			if new_credits_remaining<=threshold:
				frappe.log_error("credits remaing")
				
	
				
				frappe.enqueue("flexledger.api.send_mail.send_low_balance_email",
				member=attendee.member,
				package=attendee.package_purchase,
				credits_remaining=new_credits_remaining,
				queue="short")
