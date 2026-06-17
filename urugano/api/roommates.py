import frappe
from frappe.utils import getdate
from frappe import _


@frappe.whitelist(allow_guest=True)
def search_roommate_listings(gender=None, location=None, min_budget=None,
                              max_budget=None, move_in=None):
    filters = {}
    if gender:
        filters["gender"] = gender
    if location:
        filters["preferred_location"] = location
    if min_budget:
        filters["minimum_budget"] = [">=", min_budget]
    if move_in:
        filters["move_in_date"] = [">=", move_in]
    if max_budget:
        filters["maximum_budget"] = ["<=", max_budget]

    return frappe.get_all("Roommate Profile", filters=filters, fields=["*"])


@frappe.whitelist(allow_guest=True)
def apply_roommate(name=None, gender=None, location=None, age=None, roommate=None,
                   min_budget=None, max_budget=None, move_in_date=None, notes=None):
    try:
        doc = frappe.new_doc("Roommate Profile")
        doc.name1 = name
        doc.gender = gender
        doc.preferred_location = location
        doc.age = age
        doc.preferred_roommate = roommate
        doc.minimum_budget = float(min_budget or 0)
        doc.maximum_budget = float(max_budget or 0)
        doc.move_in_date = getdate(move_in_date)
        doc.additional_notes = notes
        doc.insert(ignore_permissions=True)

        return {"status": "success", "message": _("Application submitted."), "name": doc.name}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Roommate Application Error")
        frappe.throw(_("An error occurred: ") + str(e))
