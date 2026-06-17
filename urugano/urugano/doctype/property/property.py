# Copyright (c) 2025, Kelvin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Property(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from urugano.urugano.doctype.gallery.gallery import Gallery

        air_conditioning: DF.Check
        backup_generator: DF.Check
        balcony: DF.Check
        bathrooms: DF.Int
        cctv: DF.Check
        description: DF.LongText | None
        elevator: DF.Check
        featured: DF.Check
        furnished: DF.Check
        gallery: DF.Table[Gallery]
        garden__yard: DF.Check
        gas_stove: DF.Check
        gym: DF.Check
        house_cleaner: DF.Check
        image: DF.AttachImage | None
        landlord: DF.Link | None
        location: DF.Link | None
        microwave: DF.Check
        no_of_rooms: DF.Int
        parking_space: DF.Check
        pet_friendly: DF.Check
        price: DF.Currency
        property_type: DF.Link | None
        published: DF.Check
        refrigerator: DF.Check
        security_guard: DF.Check
        solar_power: DF.Check
        swimming_pool: DF.Check
        title: DF.Data
        tv: DF.Check
        washing_machine: DF.Check
        wifi: DF.Check
    # end: auto-generated types