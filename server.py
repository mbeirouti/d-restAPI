from flask import Flask, request, jsonify, redirect, make_response, render_template

from controller.backend_controller import get_patients_page, add_patient_to_database, get_patient_by_id

import json

app = Flask(__name__)


# Flask App Configuration Parameters:
# app.config['SERVER_NAME'] = 'users.dialogue.co/v1'
app.config['SERVER_NAME'] = 'localhost:5000'

page = None

@app.route('/patients', methods=["GET", "POST"])
def handle_patients_URL():
	if request.method == "GET":
		
		page = request.args.get("page")
		# If no query parameter was provided
		if page == None:
			# Redirect to first page
			return redirect("http://" + app.config['SERVER_NAME'] + "/patients?page=1")
		else:
			# Acquire specified page
			function_response = get_patients_page(int(page))
			# Build and return response
			response = jsonify(function_response[0])
			response.status_code = function_response[1]

			return response

	elif request.method == "POST":
		# Attempt to create patient profile using helper function
		function_response = add_patient_to_database(request.json)

		response = jsonify(function_response[0])
		response.status_code = function_response[1]

		return response


@app.route('/patients/<int:patient_id>', methods=["GET"])
def get_individual_patient(patient_id):
	if request.method == "GET":
		# Return JSON for a single patient
		function_response = get_patient_by_id(patient_id)

		response = jsonify(function_response[0])
		response.status_code = function_response[1]

		return response

	else:
		# Return a method not allowed
		response = make_response()
		response.status_code = 405

		return response

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404