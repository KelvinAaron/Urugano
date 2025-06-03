import frappe

def get_context(context):
    context.features = frappe.get_all("Property", 
                                      fields=["*"],
                                      filters={"published": 1,
                                               "featured": 1})
    return context