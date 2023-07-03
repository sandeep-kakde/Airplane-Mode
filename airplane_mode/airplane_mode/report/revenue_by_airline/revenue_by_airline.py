# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = get_columns(), get_data()
    chart = get_chart_data(data)
    report_summary = get_report_summary(data)
    return columns, data, None, chart, report_summary


def get_data():
    return frappe.db.sql(
        """
      SELECT
        airplane.airline AS "Airline",
        SUM(ticket.total_amount) AS "Revenue"
      FROM
        `tabAirplane` airplane
      LEFT JOIN
          `tabAirplane Flight` flight
        ON
          airplane.name = flight.airplane
      LEFT JOIN
        `tabAirplane Ticket` ticket
      ON
        flight.name =  ticket.flight
      GROUP BY
        Airline
      ORDER BY
        Revenue DESC
		""",
        as_dict=1,
    )


def get_columns():
    return [
        {
            "fieldname": "Airline",
            "label": "Airline",
            "fieldtype": "Link",
            "options": "Airplane",
            "width": 120
        },
        {
            "fieldname": "Revenue",
            "label": "Revenue",
            "fieldtype": "Currency",
            "width": 120
        },
    ]


def get_chart_data(data):
    labels = [d.get("Airline") for d in data]
    datasets = [{"values": [d.get("Revenue") for d in data]}]

    chart = {"data": {"labels": labels, "datasets": datasets}}
    chart["type"] = "donut"

    return chart


def get_report_summary(data):
    total = 0.0
    for d in data:
        total += d["Revenue"] if d["Revenue"] else 0

    return [
        {
            "value": total,
            "label": "Total Revenue",
            "datatype": "Currency",
            "currency": "INR",
            "indicator": "Green",
        },
    ]
