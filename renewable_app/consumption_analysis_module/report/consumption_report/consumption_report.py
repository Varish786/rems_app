# Copyright (c) 2024, varish and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# consumption_report.py
import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    
    # Define columns
    columns = [
        {"fieldname": "consumer_id", "label": "Consumer ID", "fieldtype": "Data", "width": 150},
        {"fieldname": "location", "label": "Location", "fieldtype": "Data", "width": 150},
        {"fieldname": "consumption_amount", "label": "Consumption Amount", "fieldtype": "Float", "width": 120},
        {"fieldname": "timestamp", "label": "Timestamp", "fieldtype": "Datetime", "width": 160},
        {"fieldname": "optimization_suggestion", "label": "Optimization Suggestion", "fieldtype": "Data", "width": 180},
    ]
    
    # Fetch data and analyze consumption patterns
    data = frappe.db.sql("""
        SELECT 
            ec.consumer_id, 
            ec.location, 
            SUM(ec.consumption_amount) AS consumption_amount, 
            ec.timestamp,
            co.suggested_actions AS optimization_suggestion
        FROM `tabEnergy Consumption Data` ec
        LEFT JOIN `tabConsumption Optimization` co ON ec.consumer_id = co.consumer_id
        GROUP BY ec.consumer_id, ec.location, ec.timestamp
        ORDER BY ec.timestamp DESC
    """)
    
    return columns, data
