import mysql.connector
import pandas as pd
import os

# Database Configuration
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="Apple#2013",
    database="sanction_management"
)

def insert_row(unit_name, cfa_sanction_no, cfa_sanction_date, total_amount, ifa_concurrence, ifa_concurrence_no, dfpds_schedule, remarks, provision_status, user_name, rejection_reason):
    try:
        cursor = db.cursor()
        query = "INSERT INTO sanction_details (unit_name, cfa_sanction_no, cfa_sanction_date, total_amount, ifa_concurrence, ifa_concurrence_no, dfpds_schedule, remarks, provision_status, user_name, rejection_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (unit_name, cfa_sanction_no, cfa_sanction_date, total_amount, ifa_concurrence, ifa_concurrence_no, dfpds_schedule, remarks, provision_status, user_name, rejection_reason))
        db.commit()
        cursor.close()
        return "Sanction details stored successfully!"
    except Exception as e:
        # Print the error message or log it for debugging
        print("Error:", e)
        # Rollback the transaction in case of an error
        db.rollback()
        # Return an error message to the user
        return "An error occurred while storing sanction details. Please try again later."


def fetch_row(cfa_sanction_no):
    try:
        cursor = db.cursor(dictionary=True)
        print("Received CFA Sanction No:", cfa_sanction_no)  # Debugging print statement
        cursor.execute("SELECT unit_name, cfa_sanction_date, total_amount, ifa_concurrence, ifa_concurrence_no, dfpds_schedule, remarks, provision_status,rejection_reason FROM sanction_details WHERE cfa_sanction_no = %s", (cfa_sanction_no,))
        result = cursor.fetchone()  # Fetch the result
        cursor.close()
        return result
    except Exception as e:
        # Print the error message or log it for debugging
        print("Error:", e)
        return None


def update_row(remarks, provision_status, cfa_sanction_no):
    try:
        cursor = db.cursor()
        print("Received Remarks:", remarks)  # Debugging print statement
        print("Received Provision Status:", provision_status)  # Debugging print statement
        print("Received CFA Sanction No:", cfa_sanction_no)  # Debugging print statement

        cursor.execute("UPDATE sanction_details SET remarks = %s, provision_status = %s WHERE cfa_sanction_no = %s",
                       (remarks, provision_status, cfa_sanction_no))
        db.commit()
        cursor.close()
        return 'Sanction details updated successfully'
    except Exception as e:
        # Print the error message or log it for debugging
        print("Error:", e)
        # Rollback the transaction in case of an error
        db.rollback()
        # Return an error message to the user
        return "An error occurred while updating sanction details. Please try again later."

def generate_excel_report(start_date, end_date):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sanction_details WHERE created_at BETWEEN %s AND %s", (start_date, end_date))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return "No data found for the given date range."

        # Convert the result to a DataFrame
        df = pd.DataFrame(rows)

        # Generate Excel file
        excel_filename = 'sanction_report.xlsx'
        # Specify the path to the Downloads folder
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        excel_filepath = os.path.join(downloads_folder, excel_filename)
        df.to_excel(excel_filepath, index=False)

        return excel_filepath

    except Exception as e:
        print("Error:", e)
        return "An error occurred while generating the Excel report."
