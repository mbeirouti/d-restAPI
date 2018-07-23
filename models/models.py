# The schema/templates for the endpoints implemented
model_json =  {
	
	"patients" : {
		"data": [],
		"links": {
			"self": "string",
			"next": "string"
		}
	},

	"patient" : {
		"attributes": {
			"email": "string",
			"first_name": "string",
			"last_name": "string",
			"birthdate": "string",
			"sex": "string"
		}
	},

	"http-error" : {
		"errors": [
			{
				"id": "string",
				"status": "string",
				"title": "string",
				"detail": "string",
				"code": "string",
				"source": {}
			}
		]
	}

}