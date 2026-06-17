import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def user_roles():
    return "Landlord" in frappe.get_roles()


@frappe.whitelist(allow_guest=True)
def create_guest_account(email=None, first_name=None, last_name=None, password=None):
    try:
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.new_password = password
        user.insert(ignore_permissions=True)
        return {"status": "success", "message": _("User account created successfully."), "email": user.email}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "User Creation Error")
        frappe.throw(_("An error occurred while creating the user account: ") + str(e))


@frappe.whitelist(allow_guest=True)
def create_landlord_account(email=None, first_name=None, last_name=None, password=None):
    try:
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.new_password = password
        user.role_profile_name = "Landlord"
        user.module_profile = "Landlord"
        user.insert(ignore_permissions=True)
        return {"status": "success", "message": _("User account created successfully."), "email": user.email}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "User Creation Error")
        frappe.throw(_("An error occurred while creating the user account: ") + str(e))
