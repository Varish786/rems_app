# Copyright (c) 2024, varish and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    
    # Define the report columns
    columns = [
        {"fieldname": "source_id", "label": "Source ID", "fieldtype": "Data", "width": 150},
        {"fieldname": "energy_type", "label": "Energy Type", "fieldtype": "Select", "width": 120},
        {"fieldname": "production_amount", "label": "Production Amount", "fieldtype": "Float", "width": 150},
        {"fieldname": "timestamp", "label": "Timestamp", "fieldtype": "Datetime", "width": 160},
    ]
    
    # Fetch the energy production data from the Energy Production Data doctype
    data = frappe.db.sql("""
        SELECT 
            source_id, 
            energy_type, 
            SUM(production_amount) AS production_amount, 
            timestamp
        FROM `tabEnergy Production Data`
        GROUP BY source_id, energy_type, timestamp
        ORDER BY timestamp DESC
    """)
    
    return columns, data




