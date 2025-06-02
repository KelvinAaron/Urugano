import frappe

def get_context(context):
    print(f"\n\n\n\{frappe.form_dict}\n\n\n")
    name = frappe.form_dict.docname
    doc = frappe.get_doc("Property", name) 
    context.doc = doc
    return context