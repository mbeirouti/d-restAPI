import re
from models.models import model_json
from copy import deepcopy

def validate_patient_data(patient_data):
	valid = True

	# Validate that all fields are present
	if ((not "attributes" in patient_data) or 
		(not "email" in patient_data["attributes"]) or
		(not "first_name" in patient_data["attributes"]) or
		(not "last_name" in patient_data["attributes"]) or
		(not "birthdate" in patient_data["attributes"]) or
		(not "sex" in patient_data["attributes"])):
		
		return False, "Missing Field"
	
	# All fields are present
	else:

		re_birthdate= re.compile("(\d{4})-(\d{2})-(\d{2})")
		re_email = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

		# TODO: Add test for empty strings in first and last name
		# Validate that they are all formatted correctly (IMPERFECT IMPLEMENTATION)
		if ((re_email.match(patient_data["attributes"]["email"]) is None) or
			(not isinstance(patient_data["attributes"]["first_name"], str)) or
			(not isinstance(patient_data["attributes"]["last_name"], str)) or
			(re_birthdate.match(patient_data["attributes"]["birthdate"]) is None) or
			(not patient_data["attributes"]["sex"] in ["M", "F"])):

			return False, "Misformatted Field"
		else:
			
			return True, "All Good"

# Using a database cursor and row, this function fills in a patient json template
def plug_patient_data_into_json(cursor, row):

	for index, column in enumerate(cursor.description):
		model_json["patient"]["attributes"][column[0]] = row[index]
	
	return deepcopy(model_json["patient"])

# Using database cursor and rows of records, this function fills in a page of patients json template
def plug_patients_into_page_json(cursor, rows):

	patients = []
	for row in rows:

		patients.append(plug_patient_data_into_json(cursor, row))

	model_json["patients"]["data"] = patients

	return deepcopy(model_json["patients"])

# Fills in the json template for an http error
def plug_http_error_into_json(error_id, status, title, detail, code, source):
	
	model_json["http-error"]["errors"][0]["id"] = error_id
	model_json["http-error"]["errors"][0]["status"] = status
	model_json["http-error"]["errors"][0]["title"] = title
	model_json["http-error"]["errors"][0]["detail"] = detail
	model_json["http-error"]["errors"][0]["code"] = code
	model_json["http-error"]["errors"][0]["source"] = source

	return deepcopy(model_json["http-error"])