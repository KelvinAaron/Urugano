import frappe
from frappe.utils import getdate
from frappe import _

@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
def apply_roommate():
    try:
        data = frappe.local.request.get_json()

        roommate = frappe.new_doc("Roommate Profile")
        roommate.name1 = data.get("name")
        roommate.gender = data.get("gender")
        roommate.preferred_location = data.get("location")
        roommate.age = data.get("age")
        roommate.preferred_roommate = data.get("roommate")
        roommate.minimum_budget = float(data.get("min_budget") or 0)
        roommate.maximum_budget = float(data.get("max_budget") or 0)
        roommate.move_in_date = getdate(data.get("move_in_date"))
        roommate.additional_notes = data.get("notes")
        roommate.insert(ignore_permissions=True)

        return {"status": "success", "message": _("Application submitted."), "name": roommate.name}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Roommate Application Error")
        frappe.throw(_("An error occurred: ") + str(e))

#    Object { name: "John Doe", gender: "male", location: "Zindiro", roommate: "Same gender", min_budget: "150000", max_budget: "200000", move_in_date: "2025-06-30", notes: "Hmm" }