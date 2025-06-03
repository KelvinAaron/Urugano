import frappe

@frappe.whitelist()
def search_properties():
    args = frappe.request.args

    filters = {}
    if args.get("property_type") and args.get("property_type") != "Property Type":
        filters["property_type"] = args.get("property_type")
    if args.get("location"):
        filters["location"] = args.get("location")
    if args.get("furnished") and args.get("furnished") != "Furnished":
        filters["furnished"] = True if args.get("furnished") == "Yes" else False
    if args.get("number_of_rooms"):
        filters["no_of_rooms"] = args.get("number_of_rooms")
    if args.get("max_price"):
        filters["price"] = ["<=", args.get("max_price")]

    results = frappe.get_all("Property", filters=filters, fields=["*"])
    return results
