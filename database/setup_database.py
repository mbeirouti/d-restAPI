import sqlite3

# Used this to create a quick 5 person database, then added stuff manually using postman
if __name__ == '__main__':
    connection = sqlite3.connect("patientDatabase.db")

    cursor = connection.cursor()

    # Create a new patient table
    # TODO: Make email primary key
    cursor.execute(
        '''CREATE TABLE patients (email TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, birthdate TEXT, sex TEXT)''')

    # List of people to add
    # TODO: Generate this automatically somehow (USE ROWID)
    people = [("dudeDudeson@gmail.com", "Dude", "Dudeson", "1990-09-22", "M"),
              ("personMcpersonface@gmail.com", "Person", "McPersonface", "1975-03-04", "M"),
              ("cooldude33@gmail.com", "Jason", "Bournette", "1977-04-04", "F"),
              ("ishyaboytpain@hotmail.com", "T", "Pain", "1980-06-07", "M"),
              ("michaelscott@yahoo.com", "Michelle", "Scott", "1989-07-12", "F")]

    # Insert rows into database
    cursor.executemany("INSERT INTO patients VALUES (?,?,?,?,?)", people)

    # Save the changes
    connection.commit()

    # Close database
    connection.close()
