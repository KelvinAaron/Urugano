import frappe

def get_context(context):
    print(f"\n\n\n\{frappe.form_dict}\n\n\n")
    name = frappe.form_dict.docname
    doc = frappe.get_doc("Property", name) 
    landlord = frappe.get_doc("Landlord", doc.landlord)
    context.landlord = landlord
    location = frappe.get_doc("Location", doc.location)
    context.location = location
    context.doc = doc
    context.gallery = doc.gallery
    # for image in doc.gallery:
    #     # image.image = frappe.utils.get_url(image.image)
    #     print(image.image)

    return context