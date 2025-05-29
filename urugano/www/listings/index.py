# your_app/www/property/index.py

import frappe

def get_context(context):
    context.properties = frappe.get_all(
        "Property",
        fields=['*'],
        order_by="creation desc"
    )
    return context