# Copyright (c) 2025, Kelvin and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class RoommateProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		additional_notes: DF.SmallText | None
		age: DF.Int
		gender: DF.Literal["Other", "Male", "Female"]
		maximum_budget: DF.Currency
		minimum_budget: DF.Currency
		move_in_date: DF.Date | None
		name1: DF.Data | None
		preferred_location: DF.Data | None
		preferred_roommate: DF.Literal["Same gender", "Any"]
		user: DF.Link | None
	# end: auto-generated types
	pass
