import frappe
from frappe import _
import json
import os


def read_monitor_log(limit=10):
    log_file_path = '/home/erp_user/frappe-bench/logs/monitor.json.log'
    
    if not os.path.exists(log_file_path):
        return {"error": "Log file not found"}
    
    try:
        with open(log_file_path, 'r') as log_file:
            log_data = []
            for line in log_file:
                if line.strip():  # Skip empty lines
                    log_data.append(json.loads(line.strip()))
                if len(log_data) >= limit:
                    break  
        
        return {
            "status": "success",
            "data": log_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def get_specific_reports(reports):
    try:

        # Structure the reports into a key-value pair format
        reports_dict = {}
        for report in reports:
            report_key = report['report_name']
            reports_dict[report_key] = {
                "name": report['name'],
                "modified": report['modified'],
                "module": report['module'],
                "doctype": report['ref_doctype']
            }

        return {"status": "success", "reports": reports_dict}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching reports"))
        return {"status": "error", "message": str(e)}

# --------------------------------------------------------------------------------
@frappe.whitelist()
def get_operator_dashboard(from_date=None, to_date=None):
    try:
        if not from_date or not to_date:
            frappe.throw(_("Please provide 'from_date' and 'to_date' filters."))

        # Fetch energy production data
        production_report = frappe.get_doc('Report', 'Energy Production Report')
        production_columns, production_data = production_report.get_data()

        # Fetch energy consumption data
        consumption_report = frappe.get_doc('Report', 'Consumption Report')
        consumption_columns, consumption_data = consumption_report.get_data()

        # Fetch maintenance alerts data with date filters
        maintenance_report = frappe.get_doc('Report', 'Maintenance Report')
        maintenance_columns, maintenance_data = maintenance_report.get_data(filters={
            'from_date': from_date,
            'to_date': to_date
        })

        # Fetch grid integration data
        grid_integration_report = frappe.get_doc('Report', 'Grid Integration Report')
        grid_columns, grid_data = grid_integration_report.get_data()

        # Structure the dashboard data
        dashboard_data = {
            "energy_production": {
                "columns": production_columns,
                "data": production_data
            },
            "energy_consumption": {
                "columns": consumption_columns,
                "data": consumption_data
            },
            "maintenance_alerts": {
                "columns": maintenance_columns,
                "data": maintenance_data
            },
            "grid_integration": {
                "columns": grid_columns,
                "data": grid_data
            }
        }

        return dashboard_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching Operator Dashboard data"))
        return {"error": str(e)}


@frappe.whitelist()
def get_admin_dashboard():
    try:
        users = frappe.get_all('RenewableEnergy_User', fields=['user_id', 'name1', 'role', 'contact_information'])

        system_monitoring_data = read_monitor_log()
        
        report_names = [
            "Consumption Report",
            "Energy Production Report",
            "Grid Integration Report",
            "Maintenance Report"
        ]
        reports_data = frappe.get_all('Report', filters={
            'report_name': ['in', report_names]
        }, fields=['name', 'report_name', 'modified', 'module', 'ref_doctype'])
        
        reports=get_specific_reports(reports_data)
        
        # Structure the dashboard data
        dashboard_data = {
            "user_management": users,
            "system_monitoring": system_monitoring_data,
            "reports": reports
        }

        return dashboard_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching Admin Dashboard data"))
        return {"error": str(e)}


@frappe.whitelist(allow_guest=True)
def get_consumption_report():
    try:
        consumption_report = frappe.get_doc('Report', 'Consumption Report')
        consumption_columns, consumption_data = consumption_report.get_data()
        
        consumption_report={"energy_consumption": {
                "columns": consumption_columns,
                "data": consumption_data
            }
          }
        return consumption_report
    except Exception as e:
        return {"status": "error", "message": str(e)}






