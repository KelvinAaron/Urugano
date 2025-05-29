import frappe

def get_context(context):
    name = frappe.get_url().split("/")[-1]
    doc = frappe.get_doc("Property", name) 
    context.doc = doc
    return context