import frappe

def get_context(context):
    name = context.route.split("/")[-1]
    doc = frappe.get_doc("Property", name) 
    context.doc = doc
    return context