# Copyright (c) 2025, Kelvin and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Property(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from urugano.urugano.doctype.amenity_item.amenity_item import AmenityItem
		from urugano.urugano.doctype.gallery.gallery import Gallery

		amenities: DF.Table[AmenityItem]
		bathrooms: DF.Int
		description: DF.LongText | None
		featured: DF.Check
		furnished: DF.Check
		gallery: DF.Table[Gallery]
		image: DF.AttachImage | None
		landlord: DF.Link | None
		location: DF.Link | None
		no_of_rooms: DF.Int
		price: DF.Currency
		property_type: DF.Link | None
		published: DF.Check
		title: DF.Data
	# end: auto-generated types
	pass
