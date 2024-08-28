# Copyright (c) 2024, varish and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# renewable_app/renewable_app/grid_integration_module/report/grid_integration_report/grid_integration_report.py

import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "integration_id", "label": "Integration ID", "fieldtype": "Data", "width": 150},
        {"fieldname": "source_id", "label": "Source ID", "fieldtype": "Link", "options": "Energy Source Configuration", "width": 150},
        {"fieldname": "grid_location", "label": "Grid Location", "fieldtype": "Data", "width": 150},
        {"fieldname": "energy_flow", "label": "Energy Flow (kWh)", "fieldtype": "Float", "width": 120},
        {"fieldname": "current_level", "label": "Storage Level (kWh)", "fieldtype": "Float", "width": 150},
        {"fieldname": "integration_efficiency", "label": "Integration Efficiency (%)", "fieldtype": "Float", "width": 150},
        {"fieldname": "timestamp", "label": "Timestamp", "fieldtype": "Datetime", "width": 150},
    ]

    query = """
        SELECT 
            gi.integration_id, gi.source_id, gi.grid_location,
            gi.energy_flow, es.current_level AS storage_level, 
            (gi.energy_flow / IFNULL(es.current_level, 1)) * 100 AS integration_efficiency, gi.timestamp
        FROM 
            `tabGrid Integration Data` gi
        LEFT JOIN 
            `tabEnergy Storage Management` es ON gi.source_id = es.source_id
        ORDER BY 
            gi.timestamp DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    return columns, data

