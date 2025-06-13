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
    amenity_icons = {}

    for amenity in doc.amenities:
        icon = None
        if amenity.icon: 
            icon = frappe.get_doc("Amenity Icon", amenity.icon)
            amenity_icons[amenity.amenity] = icon  
    context.amenity_icons = amenity_icons
    return context