# hbnb


Project Directory Structure:
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md



# Describe purpose of each directory and file

Directories and Subdirectories:
	app/
	Contains the core application code
		__init.py__

		api/
		Houses the API endpoints, organised by version (v1/)
			vi/
				*** include files ***
			__init.py__

		models/
		Contains business logic classes (e.g., user.py, place.py)
			*** include files ***

		services/
		Implementation of Facade pattern which manages the interaction between layers
			*** include files ***

		persistence/
		Implementation of in-memory repository. This is later replaced by a database-backed solution using SQL Alchemy.
			*** include files ***


Root Files:
	run.py - entry point for running Flask application

	config.py - configuring environment variables and application settings

	requirements.txt - lists all Python packages needed for project

	README.md - this! (contains brief overview of the project)




# Include instructions on how to install dependencies and run the application
...
...
...