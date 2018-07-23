import controller.backend_controller as bec
import controller.helper_functions as hf
import sqlite3


def test_validate_patient_data():
    passes_all = True

    tests = [{"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": "Matthew", "last_name": "Beirouti",
                             "birthdate": "1993-09-12", "sex": "M"}},
             {"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": "Matthew", "last_name": "Beirouti",
                             "birthdate": "1993-09-12", "sex": "Ff"}},
             {"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": "Matthew", "last_name": "Beirouti",
                             "birthdate": "1993-092", "sex": "M"}},
             {"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": "Matthew", "last_name": 0,
                             "birthdate": "1993-09-12", "sex": "M"}},
             {"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": 1, "last_name": "Beirouti",
                             "birthdate": "1993-09-12", "sex": "M"}},
             {"attributes": {"email": "matthewbeirouti@gmailcom", "first_name": "Matthew", "last_name": "Beirouti",
                             "birthdate": "1993-09-12", "sex": "M"}},
             {"email": "matthewbeirouti@gmail.com", "first_name": "Matthew", "last_name": "Beirouti",
              "birthdate": "1993-09-12", "sex": "M"}]

    results = [True, False, False, False, False, False, False]

    for test in enumerate(tests):

        if bec.validate_patient_data(test[1])[0] != results[test[0]]:
            passes_all = False

    assert passes_all, "Patient validation failing"


def test_add_patient_to_database():
    passes_all = True

    tests = [{"attributes": {"email": "temporaryperson@gmail.com", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "temporarypersonil.com", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "temporaryperson@gmailom", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "temporaryperson@gmail.com", "first_name": 1, "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "temporaryperson@gmail.com", "first_name": "Temp", "last_name": 2,
                             "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "temporaryperson@gmail.com", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-22", "sex": "F"}},
             {"attributes": {"email": "temporaryperson@gmail.com", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "A"}},
             {"attributes": {"first_name": "Temp", "last_name": "Person", "birthdate": "1800-08-22", "sex": "F"}},
             {"attributes": {"email": "matthewbeirouti@gmail.com", "first_name": "Temp", "last_name": "Person",
                             "birthdate": "1800-08-22", "sex": "F"}},
             ]

    results = [{"attributes": {"email": "temporaryperson@gmail.com", "first_name": "Temp", "last_name": "Person",
                               "birthdate": "1800-08-22", "sex": "F"}},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The data sent in the request was invalid",
                            "id": "Some Request Number", "source": None, "status": 400, "title": "Bad Request"}]},
               {"errors": [{"code": "Some Error Code", "detail": "The email already exists in the database",
                            "id": "Some Request Number", "source": None, "status": 409, "title": "Conflict"}]}]

    for test in enumerate(tests):
        # print(validate_patient_data(test[1]))
        if bec.add_patient_to_database(test[1])[0] != results[test[0]]:
            # print(test)
            passes_all = False

    # Remove added temporaryperson@gmail.com to ensure test runs smoothly next time
    connection = sqlite3.connect("./database/patientDatabase.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM patients WHERE email=?", ("temporaryperson@gmail.com",))

    connection.commit()

    connection.close()

    assert passes_all, "Failed test in add_patient_to_database"


def test_get_patient_by_id():
    passes_all = True
    tests = [1, 5, 22, 42]
    results = [{"attributes": {"birthdate": "1990-09-22", "email": "dudeDudeson@gmail.com", "first_name": "Dude",
                               "last_name": "Dudeson", "sex": "M"}},
               {"attributes": {"birthdate": "1989-07-12", "email": "michaelscott@yahoo.com", "first_name": "Michelle",
                               "last_name": "Scott", "sex": "F"}},
               {"attributes": {"birthdate": "1993-09-12", "email": "12@yahoo.org", "first_name": "Matthew",
                               "last_name": "Beirouti", "sex": "M"}},
               {"errors": [{"code": "Some Error Code", "detail": "The patient with ID 42 was not found",
                            "id": "Some Request Number", "source": None, "status": 404, "title": "Not Found"}]}]
    for test in enumerate(tests):

        if bec.get_patient_by_id(test[1])[0] != results[test[0]]:
            passes_all = False

    assert passes_all, "Failed test in get_patient_by_id"


def test_get_patients_page():
    passes_all = True
    tests = [2, 42]
    results = [{"data": [{"attributes": {"birthdate": "1993-09-12", "email": "1@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "2@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "3@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "4@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "5@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "6@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "7@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "8@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "9@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}},
                         {"attributes": {"birthdate": "1993-09-12", "email": "10@yahoo.org", "first_name": "Matthew",
                                         "last_name": "Beirouti", "sex": "M"}}],
                "links": {"next": "http://localhost:5000/patients?page=3",
                          "self": "http://localhost:5000/patients?page=2"}},
               {"data": [], "links": {"next": "http://localhost:5000/patients?page=43",
                                      "self": "http://localhost:5000/patients?page=42"}}]

    for test in enumerate(tests):

        if bec.get_patients_page(test[1])[0] != results[test[0]]:
            passes_all = False

    assert passes_all, "Failed test in get_patients_page"


# Functions below are integration tested above but can also be unit tested here
def test_plug_patient_data_into_json():
    pass


def test_plug_patients_into_page_json():
    pass


def test_plug_http_error_into_json():
    pass


if __name__ == "__main__":
    test_validate_patient_data()

    test_add_patient_to_database()

    test_get_patient_by_id()

    test_get_patients_page()

    # test_plug_patient_data_into_json()

    # test_plug_patients_into_page_json()

    # test_plug_http_error_into_json()

    print("All tests ran successfully")
