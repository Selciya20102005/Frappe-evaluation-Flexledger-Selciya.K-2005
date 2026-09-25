Group B — ORM Internals & Query Builder
B2c — Dangerous Patterns
document lifecycle bugs
3 pts
The snippet below has two bugs related to document lifecycle. Identify both and write the corrected version in README_internals.md:

def validate(self):
    self.total_charged = sum(r.credits_charged for r in self.attendees)
    self.save()
    pkg = frappe.get_doc("Package Purchase", self.package_purchase)
    pkg.credits_used += self.total_charged
    pkg.save()


Answer:
def validate(self):
    self.total_charged = sum(r.credits_charged for r in self.attendees)
def on_update(self):
    pkg = frappe.get_doc("Package Purchase", self.package_purchase)
    pkg.credits_used += self.total_charged
    pkg.save()

In validate function calculation/validation should be performed whereas database side effects like updating should be in respective lifecycle event



B2d — Concurrency, One Question
optimistic locking
1 pt
In README_internals.md: two front-desk staff open the same Package Purchase at once and both try to save a change. Why would you see a "Document has been modified after you have opened it" error, and how does Frappe prevent one of them from silently overwriting the other's edit? (One paragraph.)


Answer:when two front-desk staff open the same package purchase both initially have the same modified time.when the first person saves frappe updates the document modified time.when the second person tries to save their older copy means frappe detects that the document has changed  and raises"document has been modified after you have opened it".this concurrency check protects the lost updates.





Group C — Schema
C3 — Attendee Entry & Package Purchase
1.rename a test Member record. Does member on linked Package Purchase records update automatically? Why or why not?

Answer:
Renaming a test member record doesn't reflected in the linked package purchase records.The change will not automatically updated in the linked doctype.For changing the name in the linked doctype we need to write the separate rename logic for that.





Group D — Roles & Permissions
D2 — Row-Level Filtering & Data Leaks
1.why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?

Answer:
Frappe.get_all usually bypasses all the permissions that was set to the doctype and returns all the documents from the particular doctype to the user.So frappe.get_all is considered to be dangerous in the whitelisted method because whitelisted method can be called from the browser itself,and in result the unauthorized users will read the records illegally.


Group E — Class Session Lifecycle
E1 — Complete Lifecycle
1.Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md.

Answer:
Actually when on_update() event  runs,frappe will automatically save the document.Adding the self.save() is not necessary.self.save() will used to trigger all the document events like validate,on_update etc so putting the self.save inside the on_update() will leads to the recursive action.

E2 — autoname & Renaming
1.Call frappe.rename_doc("Member", old, new, merge=False) in a utility function and show linked fields update automatically. Explain when merge=True would be dangerous.

Answer:
merge=False will be used to allow the renaming the document to the already existing documents name.In that case the merge=False will makes the overriding of the document values,the renamed document values will be existed.whereas merge=True will raise an exception as like the "document is already present".


E3 — One Performance Judgment Call
frappe.db.get_value vs get_doc
2 pts
Inside the balance-check loop in validate(), which pattern would you use to read the cancellation window from Studio Settings, and why?

doc = frappe.get_doc("Studio Settings", "Studio Settings")
window = doc.default_cancellation_window_hours

window = frappe.db.get_value("Studio Settings", None, "default_cancellation_window_hours")


Answer:
For reading the field in the single doctype I usually use window = frappe.db.get_value("Studio Settings", None, "default_cancellation_window_hours").This will used to read the field of the studio settings doctype directly without storing the document in any variables.It will reduces the usuage of many variables which will be reducing the occupancy of the many variables in the doctype which will help in avoiding the unauthorization.



Group H — Client Scripts
H1 — Class Session Form Script
In README_internals.md: why does a frappe.call inside the validate client event not work, and why must async fetches happen in onload/refresh instead?
frappe.call() is tha asynchronous function whereas validate will run synchronously before saving so the server response arrives too late to affect the validation.so we need to use onload/refresh for asynchronous data fetching and then we can use the fetched data during validation.



Group I — Reports
I1 — Query Report: Members Running Low
In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

Answer:the parameterized version is always preferred because the values are passed separately from the sql statement ,this prevents the sql injection and we can protect our data safely from the unauthorized users and the hacking activities



Group J — Print Format
J1 — Package Receipt
In README_internals.md: explain the difference between putting a frappe.get_all() call directly inside the Jinja template versus pre-computing in before_print() and referencing doc.precomputed_field.

Answer:
calling the frappe.get_all() directly inside a jinja template performs database work during the rendering process and mixes the reading logic.pre-computing the data in before_print() keeps the database logic in python itself and allows the template simply refer to the doc.precomputed_field.



Group K — Scheduled Jobs & Performance
K2 — Spot the N+1
bulk fetch vs per-row query
3 pts
The snippet below has an N+1 query problem. Identify it and rewrite it:

# N+1 PROBLEM - fix this
sessions = frappe.get_all("Class Session", fields=["name","trainer"])
for s in sessions:
    trainer = frappe.get_doc("Trainer", s.trainer)
    print(trainer.trainer_name, trainer.phone)
Bulk operations, manual indexing, and report query-profiling are real skills too — they're in Bonus once this pattern is second nature.


Answer:
import frappe
def print_session_trainers():
 sessions=frappe.get_all("Class Session",fields=["name","trainer"])
 trainer_name=list(set(s.trainer for s in sessions if s.trainer))
 trainers=frappe.get_all("Trainer",filters={"name":["in",trainer_name]},fields=["name","trainer_name","phone"])
 trainer_map{
    trainer.name:trainer for trainer in trainers
 }
 for s in sessions:
  trainer=trainer_map.get(s.trainer)
  if trainer:
   print(trainer.trainer_name,trainer.phone)

Actually the above code uses two queries to fetch the details of the trainers from the class session.The storage of the class session records in the set used to avoid the duplicate records and the trainer records are collected and stored in the dictionary for the storage of the records in the object memory.




Group L — REST API

 curl -X GET "http://127.0.0.1:8000/api/resource/Member/MEM-2026-0007
"\-H "Authorization:token b7b7c733640dd73:69d30d9d8b8835d"

{
    "data": {
        "name": "MEM-2026-0007",
        "owner": "Administrator",
        "creation": "2026-09-25 13:53:16.244796",
        "modified": "2026-09-25 13:53:16.244796",
        "modified_by": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "member_name": "guiiii",
        "phone": "+91-2222222222",
        "email": "selciya.k2005@gmail.com",
        "join_date": "2026-09-25",
        "status": "Active",
        "doctype": "Member"
    }
}




http://127.0.0.1:8000/api/method/flexledger.api.custom_whitelisted_method.get_member_balance?member

{
    "message": {
        "member": "MEM-2026-0006",
        "credits_remaining": 0,
        "expiry_date": null
    }
}


http://127.0.0.1:8000/api/resource/Member/MEM-2026-0000?autho

404 NOT FOUND
{
    "exc_type": "DoesNotExistError",
    "_server_messages": "[\"{\\\"message\\\":\\\"Member MEM-2026-0000 not found\\\",\\\"as_table\\\":false,\\\"title\\\":\\\"Message\\\",\\\"indicator\\\":\\\"red\\\",\\\"raise_exception\\\":1,\\\"__frappe_exc_id\\\":\\\"52345bc76650a25a200c8a6cb7ddd1eee2308caf12439a0ccef952d6\\\"}\"]"
}



Demo Video

https://drive.google.com/file/d/1JQu-ELfnsR5aH2ksRAYpKArrWbZTlloi/view?usp=sharing

