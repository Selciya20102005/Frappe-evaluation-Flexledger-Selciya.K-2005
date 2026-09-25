import frappe
def print_session_trainers():
    sessions=frappe.get_all("Class Session",fields=["name","trainer"])
    trainer_name=list(set(s.trainer for s in sessions if s.trainer))
    trainers=frappe.get_all("Trainer",filters={"name":["in",trainer_name]},fields=["name","trainer_name","phone"])
    trainer_map={
        trainer.name:trainer for trainer in trainers
    }
    for s in sessions:
        trainer=trainer_map.get(s.trainer)
        if trainer:
            print(trainer.trainer_name,trainer.phone)