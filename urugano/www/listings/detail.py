import frappe

def get_context(context):
    print(f"\n\n\n\{frappe.form_dict}\n\n\n")
    name = frappe.form_dict.docname
    doc = frappe.get_doc("Property", name) 
    context.doc = doc
    landlord = frappe.get_doc("Landlord", doc.landlord)
    context.landlord = landlord
    location = frappe.get_doc("Location", doc.location)
    context.location = location

    for amenity in doc.amenities:
        icon = None
        if amenity.icon: 
            icon = amenity.icon 
    context.icon = icon

    context.properties = frappe.get_all(
        "Property",
        fields=['*'],
        order_by="creation desc"
    )

    return context