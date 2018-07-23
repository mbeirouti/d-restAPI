# User API (d-restAPI)

Implementation of swagger specifications

## Getting Started

### Prerequisites

This implementation uses the latest version of Python (3.7) and Flask. Install flask using the following command. 

```
pip install Flask
```

## Running the Server

Assuming you are using Windows, open cmd and navigate into the project directory. Set the Flask environment variable using the *exact* code below:
```
set FLASK_APP=server.py
```

Run the server using:
```
flask run
```

The server should start on http://localhost:5000/ and you can now access the API (locally).


## Tests

Tests can be run by navigating to the project directory in cmd and running the following.
```
python test_backend.py
```