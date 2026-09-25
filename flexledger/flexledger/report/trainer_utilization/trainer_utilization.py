import frappe
def execute(filters=None):
	filters=filters or {}
	conditions={
		"session_date":["between",[filters.get("from_date"),filters.get("to_date")]],
		"docstatus":1
	}
	if filters.get("trainer"):
		conditions["trainer"]=filters["trainer"]
	sessions=frappe.get_list("Class Session",filters=conditions,fields=["name","trainer"])
	data={}
	for session in sessions:
		trainer=session.trainer
		if trainer not in data:
			data[trainer]={
				"trainer":trainer,
				"sessions_run":0,
				"total_attendees":0,
				"no_shows":0,
				"credits_processed":0
			}
		data[trainer]["sessions_run"]+=1
		session_doc=frappe.get_doc("Class Session",session.name)
		for attendee in session_doc.attendees:
			data[trainer]["total_attendees"]+=1
			if attendee.attendance_status=="No-Show":
				data[trainer]["no_shows"]+=1
			data[trainer]["credits_processed"]+=(attendee.credits_charged or 0)
	rows=[]
	for row in data.values():
		rate=(
			row["no_shows"]/row["total_attendees"]*100
			if row["total_attendees"] else 0
		)
		rows.append({
			"trainer":row["trainer"],
			"sessions_run":row["sessions_run"],
			"total_attendees":row["total_attendees"],
			"no_show_rate":rate,
			"credits_processed":row["credits_processed"]

		})
	columns=[
		{"label":"Trainer","fieldname":"trainer","fieldtype":"Link","options":"Trainer"},
		{"label":"Sessions Run","fieldname":"sessions_run","fieldtype":"Int"},
		{"label":"Total Attendees","fieldname":"total_attendees","fieldtype":"Int"},
		{"label":"No-show Rate %","fieldname":"no_show_rate","fieldtype":"Percent"},
		{"label":"Credits Processed","fieldname":"credits_processed","fieldtype":"Float"}
	]
	return columns,rows