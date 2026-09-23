# Copyright (c) 2026, selciya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate,today


class ClassSession(Document):
	
	def validate(self):
		self.validate_session_date()
		credits_required = self.get_required_credits()

		for attendee in self.attendees:
			self.validate_attendee(attendee, credits_required)

	def validate_session_date(self):
		if not self.session_date:
			frappe.throw("Session Date is required")

		if self.status == "Draft":
			if getdate(self.session_date) < getdate(today()):
				frappe.throw(
					"Session Date cannot be in the past for a Draft Class Session."
				)

	def get_required_credits(self):
		if not self.session_type:
			frappe.throw("Session Type is required")

		credits_required = frappe.db.get_value(
			"Session Type",
			self.session_type,
			"credits_required"
		)

		if credits_required is None:
			frappe.throw(
				f"Credits Required is not configured for Session Type {self.session_type}."
			)

		credits_required = int(credits_required)

		if credits_required <= 0:
			frappe.throw(
				f"Credits Required must be greater than 0 for Session Type {self.session_type}."
			)

		return credits_required

	def validate_attendee(self, attendee, credits_required):
		if not attendee.member:
			frappe.throw(
				f"Member is required in attendee row {attendee.idx}."
			)

		if not attendee.package_purchase:
			frappe.throw(
				f"Package Purchase is required for member {attendee.member}."
			)

		package = frappe.get_doc(
			"Package Purchase",
			attendee.package_purchase
		)

		if package.member != attendee.member:
			frappe.throw(
				f"Package {package.name} does not belong to member {attendee.member}."
			)

		if package.status != "Active":
			frappe.throw(
				f"Package {package.name} is not Active."
			)

		if not package.expiry_date:
			frappe.throw(
				f"Package {package.name} does not have an expiry date."
			)

		if getdate(package.expiry_date) < getdate(self.session_date):
			frappe.throw(
				f"Package {package.name} is expired."
			)

		credits_remaining = package.credits_remaining or 0

		if credits_remaining < credits_required:
			frappe.throw(
				f"Member {attendee.member} does not have enough credits. "
				f"Remaining balance: {credits_remaining}. "
				f"Required: {credits_required}."
			)

		attendee.credits_charged = credits_required

	def before_submit(self):
		if self.status != "Completed":
			frappe.throw(
				"Class Session can only be submitted when Status is Completed."
			)

		for attendee in self.attendees:
			if attendee.attendance_status == "Booked":
				frappe.throw(
					f"Attendee {attendee.member} is still marked as Booked."
				)

			if not attendee.attendance_status:
				frappe.throw(
					f"Attendance Status is required for member {attendee.member}."
				)

		credits_required = self.get_required_credits()

		for attendee in self.attendees:
			attendee.credits_charged = credits_required

	def on_submit(self):
		studio_settings = frappe.get_single("Studio Settings")

		no_show_forfeits_credit = bool(
			studio_settings.no_show_forfeits_credit
		)

		for attendee in self.attendees:
			should_charge = False

			if attendee.attendance_status == "Attended":
				should_charge = True

			elif (
				attendee.attendance_status == "No-Show"
				and no_show_forfeits_credit
			):
				should_charge = True

			if not should_charge:
				attendee.credits_charged = 0
				continue

			self.deduct_attendee_credits(
				attendee,
				studio_settings
			)

	def deduct_attendee_credits(self, attendee, studio_settings):
		credits_charged = attendee.credits_charged or 0

		if credits_charged <= 0:
			return

		package = frappe.db.get_value(
			"Package Purchase",
			attendee.package_purchase,
			[
				"member",
				"total_credits",
				"credits_used",
				"credits_remaining",
				"status"
			],
			as_dict=True
		)

		if not package:
			frappe.throw(
				f"Package Purchase {attendee.package_purchase} does not exist."
			)

		if package.member != attendee.member:
			frappe.throw(
				f"Package {attendee.package_purchase} does not belong "
				f"to member {attendee.member}."
			)

		credits_remaining = package.credits_remaining or 0
		credits_used = package.credits_used or 0
		total_credits = package.total_credits or 0

		if credits_remaining < credits_charged:
			frappe.throw(
				f"Member {attendee.member} does not have enough credits. "
				f"Remaining: {credits_remaining}. "
				f"Required: {credits_charged}."
			)

		new_credits_used = credits_used + credits_charged
		new_credits_remaining = max(
			total_credits - new_credits_used,
			0
		)

		if new_credits_used > total_credits:
			frappe.throw(
				f"Package {attendee.package_purchase} cannot be charged."
			)

		new_status = (
			"Fully Used"
			if new_credits_remaining == 0
			else "Active"
		)

		frappe.db.set_value(
			"Package Purchase",
			attendee.package_purchase,
			{
				"credits_used": new_credits_used,
				"credits_remaining": new_credits_remaining,
				"status": new_status
			},
			update_modified=False
		)

		threshold = studio_settings.low_balance_alert_threshold or 0

		if new_credits_remaining <= threshold:
			frappe.enqueue(
				"flexledger.api.send_low_balance_email",
				member=attendee.member,
				package=attendee.package_purchase,
				credits_remaining=new_credits_remaining,
				queue="short"
			)

	def on_cancel(self):
		for attendee in self.attendees:
			credits_to_restore = attendee.credits_charged or 0

			if credits_to_restore <= 0:
				continue

			if not attendee.package_purchase:
				continue

			package = frappe.db.get_value(
				"Package Purchase",
				attendee.package_purchase,
				[
					"total_credits",
					"credits_used",
					"credits_remaining",
					"status"
				],
				as_dict=True
			)

			if not package:
				frappe.throw(
					f"Package Purchase {attendee.package_purchase} "
					f"could not be found."
				)

			credits_used = package.credits_used or 0
			credits_remaining = package.credits_remaining or 0
			total_credits = package.total_credits or 0

			new_credits_used = max(
				credits_used - credits_to_restore,
				0
			)

			new_credits_remaining = min(
				credits_remaining + credits_to_restore,
				total_credits
			)

			frappe.db.set_value(
				"Package Purchase",
				attendee.package_purchase,
				{
					"credits_used": new_credits_used,
					"credits_remaining": new_credits_remaining,
					"status": "Active"
				},
				update_modified=False
			)

		self.db_set("status", "Cancelled")

	def on_trash(self):
		if self.status not in ["Draft", "Cancelled"]:
			frappe.throw(
				f"Class Session {self.name} cannot be deleted. "
				f"Only Draft or Cancelled sessions can be deleted."
			)

					
			

		


