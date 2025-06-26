import frappe

def get_context(context):
    context.roommates = frappe.get_all(
        "Roommate Profile",
        fields= ["*"]
    )
    return context