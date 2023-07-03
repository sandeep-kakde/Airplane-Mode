# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):
	def before_insert(self):
		flight_name = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		flight_capacity = frappe.db.get_value("Airplane", flight_name, "capacity")
		airplane_tickets_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})

		if airplane_tickets_count >= flight_capacity:
			frappe.throw("Flight is full")

	def validate(self):
		unique_add_ons = []
		add_ons = []
		for add_on in self.add_ons:
			if add_on.item not in unique_add_ons:
				add_ons.append(add_on)
				unique_add_ons.append(add_on.item)

		self.add_ons = add_ons


	def before_save(self):
		# random_integer = str(random.randint(0, 9))
		# random_alphabet = random.choice(['A', 'B', 'C', 'D', 'E'])
		# self.seat = random_integer + random_alphabet
		total_amount = 0.0
		for add_on in self.add_ons:
			total_amount += add_on.amount

		self.total_amount = total_amount + self.flight_price

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Flight not boarded")