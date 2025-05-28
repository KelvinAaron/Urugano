# your_app/www/property/index.py

import frappe

def get_context(context):
    context.items = frappe.get_all(
        "Property",
        fields=["name", "price", "img_1", "description"],
        order_by="creation desc"
    )
    return context
