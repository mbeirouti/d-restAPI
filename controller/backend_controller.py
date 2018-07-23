import sqlite3

from models.models import model_json
from controller.helper_functions import validate_patient_data, plug_patient_data_into_json, plug_patients_into_page_json, plug_http_error_into_json

patients_per_page = 10


# TODO: Change to a global connection to avoid connecting and disconnecting in each function
def connect_to_database(database_name):

	if database_name[-3:] != ".db":
		database_name = database_name + ".db"

	connection = sqlite3.connect(database_name)

	# TODO: Do we return cursor or connection?
	return connection


# TODO: Ask how is user supposed to know the ID if there isn't a ID field in json model
def get_patient_by_id(patient_id):

	# Connect to the Database
	connection = connect_to_database("./database/patientDatabase.db")
	cursor = connection.cursor()

	# Retrieve Patient from Database
	database_response = cursor.execute("SELECT * FROM patients WHERE rowid=?", (patient_id,))
	retrieved_data = database_response.fetchone()

	if retrieved_data:

		# Plug Patient Data into model
		response = plug_patient_data_into_json(database_response, retrieved_data)
		
		return response, 200

	else:

		# Patient with specified ID doesn't exist, return http-error
		response = plug_http_error_into_json("Some Request Number",
											 404, "Not Found",
											 "The patient with ID {} was not found".format(patient_id),
											  "Some Error Code",
											   None)

		return response, 404

def add_patient_to_database(patient_data):

	data_is_valid = validate_patient_data(patient_data)

	if data_is_valid[0]:
		
		# Connect to the database
		connection = connect_to_database("./database/patientDatabase.db")
		cursor = connection.cursor()


		# Check database to see if the email exists already
		database_response = cursor.execute("SELECT * FROM patients WHERE email=?", (patient_data["attributes"]["email"], ))

		# The database does not already contain a row with this email
		if database_response.fetchone() == None:
			
			# Insert the row
			cursor.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?)", 
				[patient_data["attributes"]["email"],
				 patient_data["attributes"]["first_name"],
				 patient_data["attributes"]["last_name"],
				 patient_data["attributes"]["birthdate"],
				 patient_data["attributes"]["sex"]])
			
			# Commit to database and close the connection
			connection.commit()
			connection.close()

			# TODO: Do I redirect to profile page or do I return patient json data in the same area?
			return patient_data, 201
	
		else:
			# The database already has a row with this email
			# Get relevant http-error object
			response = plug_http_error_into_json("Some Request Number",
												 409,
												 "Conflict",
												 "The email already exists in the database",
												 "Some Error Code",
												 None)

			return response, 409
	else:
		# Data is invalid
		# Return a relevant http-error object
		response = plug_http_error_into_json("Some Request Number",
											 400,
											 "Bad Request",
											 "The data sent in the request was invalid",
											 "Some Error Code",
											 None)
		return response, 400

def get_patients_page(page_number):

	# Connect to Database
	connection = connect_to_database("./database/patientDatabase.db")
	cursor = connection.cursor()

	# Fetch 10 patients from specific page of patients
	database_response = cursor.execute("SELECT * FROM patients ORDER BY rowid LIMIT ? OFFSET ?", [patients_per_page, (page_number-1)*10])
	retrieved_data = cursor.fetchall()

	# Close connection with Database
	connection.close()

	# Place retrieved rows into patients template
	response = plug_patients_into_page_json(database_response, retrieved_data)
	
	# TODO: Change from hardcoded links to global variable that this file and server.py use
	response["links"]["self"] = "http://localhost:5000/patients?page={}".format(page_number)
	response["links"]["next"] = "http://localhost:5000/patients?page={}".format(page_number+1)

	return response, 200


if __name__ == '__main__':
	get_patients_page(1)