# Copyright (c) 2024, varish and contributors
# For license information, please see license.txt



import frappe

def execute(filters=None):
    if filters is None:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    if not from_date or not to_date:
        frappe.throw("Please provide 'from_date' and 'to_date' filters.")

    columns = [
        {"fieldname": "equipment_id", "label": "Equipment ID", "fieldtype": "Link", "options": "Energy Source Configuration", "width": 150},
        {"fieldname": "maintenance_date", "label": "Maintenance Date", "fieldtype": "Date", "width": 150},
        {"fieldname": "maintenance_type", "label": "Maintenance Type", "fieldtype": "Select", "options": "Preventive\nCorrective", "width": 150},
        {"fieldname": "alert_id", "label": "Alert ID", "fieldtype": "Data", "width": 150},
        {"fieldname": "issue_description", "label": "Issue Description", "fieldtype": "Text", "width": 200},
        {"fieldname": "alert_date", "label": "Alert Date", "fieldtype": "Date", "width": 150}
    ]

    query = """
        SELECT 
            ms.equipment_id, ms.maintenance_date, ms.maintenance_type,
            ma.alert_id, ma.issue_description, ma.alert_date
        FROM 
            `tabEnergy Maintenance Schedule` ms
        LEFT JOIN 
            `tabMaintenance Alert` ma ON ms.equipment_id = ma.equipment_id
        WHERE 
            ms.maintenance_date >= %s AND ms.maintenance_date <= %s
        ORDER BY 
            ms.maintenance_date DESC
    """

    data = frappe.db.sql(query, (from_date, to_date), as_dict=True)

    return columns, data

