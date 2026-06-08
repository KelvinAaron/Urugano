import frappe

def get_context(context):
    filters = {}

    property_type = frappe.form_dict.get("property_type")
    location = frappe.form_dict.get("location")
    furnished = frappe.form_dict.get("furnished")
    number_of_rooms = frappe.form_dict.get("number_of_rooms")
    max_price = frappe.form_dict.get("max_price")

    if property_type and property_type != "Property Type":
        filters["property_type"] = property_type

    if location:
        filters["location"] = location

    if furnished and furnished != "Furnished":
        filters["furnished"] = True if furnished == "Yes" else False

    if number_of_rooms:
        filters["no_of_rooms"] = number_of_rooms

    if max_price:
        filters["price"] = ["<=", max_price]



    context.properties = frappe.get_all(
        "Property",
        fields=['*'],
        filters=filters,
        order_by="creation desc"
    )
    return context