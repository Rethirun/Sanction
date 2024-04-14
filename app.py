from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file  # Add send_file and redirect
import os
from db_functions import insert_row, fetch_row, update_row, generate_excel_report

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database Configuration
# This part should be moved to insert_row.py for better organization

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        print(request.form)  # Debug statement to see the form data
        username = request.form.get('username')
        designation = request.form.get('designation')
        
        if username is None or designation is None:
            # Handle case where username or designation is missing
            return "Invalid request", 400
        
        designation = designation.lower()  # Ensure consistent casing for comparison
        
        if designation == 'auditor':
            # Redirect to the sanction details edit page with username and designation parameters
            return redirect(url_for('sanction_details_edit', username=username, designation=designation))
        elif designation == 'admin':
            # Redirect to the report generation page  with username and designation parameters
            return redirect(url_for('generate_report', username=username, designation=designation))
        else:
            # Redirect to the sanction details edit page with username and designation parameters
            return redirect(url_for('fetch_sanction_details', username=username, designation=designation))

    return render_template('login_page.html')

# Route for Sanction Details Edit Page
@app.route('/sanction_details_edit', methods=['GET', 'POST'])
def sanction_details_edit():
    user_name = request.args.get('username')
    designation = request.args.get('designation')

    if request.method == 'POST':
        unit_name = request.form.get('unitName')
        cfa_sanction_no = request.form.get('cfaSanctionNo')
        cfa_sanction_date = request.form.get('cfaSanctionDate')
        total_amount = request.form.get('totalAmount')
        ifa_concurrence = request.form.get('ifaConcurrence')
        ifa_concurrence_no = request.form.get('ifaConcurrenceNo')
        dfpds_schedule = request.form.get('dfpdsSchedule')
        remarks = request.form.get('remarks')
        provision_status = request.form.get('provisionStatus')
        user_name = request.form.get('actionedBy')
        rejection_reason = request.form.get('rejectionReason')

        # Replace None values with an empty string
        ifa_concurrence_no = ifa_concurrence_no if ifa_concurrence_no else ''
        remarks = remarks if remarks else ''
        rejection_reason = rejection_reason if rejection_reason else ''

        # Call the insert_row function
        result = insert_row(unit_name, cfa_sanction_no, cfa_sanction_date, total_amount, ifa_concurrence, ifa_concurrence_no, dfpds_schedule, remarks, provision_status, user_name, rejection_reason)
        print(result)  # Debug statement to check the result
        return jsonify({'message': result})

    return render_template('sanction_details_edit.html')


@app.route('/fetch_sanction_details', methods=['GET', 'POST'])
def fetch_sanction_details():
    if request.method == 'POST':
        cfa_sanction_no = request.form.get('cfaSanctionNo')

        # Call the fetch_row function
        result = fetch_row(cfa_sanction_no)
        print("Fetched Result:", result)  # Debugging print statement

        if result:
            # Consume the result
            data = {
                'unitName': result['unit_name'],
                'cfaSanctionDate': result['cfa_sanction_date'].isoformat(),  # Convert datetime.date to string
                'totalAmount': str(result['total_amount']),  # Convert Decimal to string
                'ifaConcurrence': result['ifa_concurrence'],
                'ifaConcurrenceNo': result['ifa_concurrence_no'],
                'dfpdsSchedule': result['dfpds_schedule'],
                'remarks': result['remarks'],
                'provisionStatus': result['provision_status'],
                'rejectionReason': result['rejection_reason']
            }
            return jsonify({'status': 'success', 'data': data})
        else:
            return jsonify({'status': 'error', 'message': 'Sanction details not found'})
    else:
        return render_template('fetch_sanction_details.html')  # Render the form page for GET requests


@app.route('/update_sanction_details', methods=['POST'])
def update_sanction_details():
    cfa_sanction_no = request.form['cfaSanctionNo']
    remarks = request.form['remarks']
    provision_status = request.form['provisionStatus']

    # Call the update_row function
    result = update_row(remarks, provision_status, cfa_sanction_no)
    return result

from flask import render_template

@app.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if start_date and end_date:
        excel_filepath = generate_excel_report(start_date, end_date)
        return send_file(excel_filepath, as_attachment=True)
    else:
        return render_template('generate_report.html')



if __name__ == '__main__':
    app.run(debug=True)
