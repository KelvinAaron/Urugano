import frappe


@frappe.whitelist(allow_guest=True)
def search_property_listings(location=None, property_type=None, max_price=None,
                              furnished=None, number_of_rooms=None):
    filters = {}
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

    return frappe.get_all("Property", filters=filters, fields=["*"])
