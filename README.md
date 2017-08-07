# Paranuara
Paranuara has the solution for Paranuara Challenge.
This application has API providing these end points:

- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}

# Requirement to run this applicaiton
This application is developed based on Python3.6/Django1.11 and mysql database, thus it is required to install Python3.6/Django1.11 and mysql before running this application. Also, you will need a apache server or nginx server to server this application as web application.

Besides, this application will use a couple of other extra libraries to support some functions. Those libraries are: dateutil, ultk.
- to install dateutil, use pip3.6 install python-dateutil
- to install ultk, use pip3.6 install nltk. After finish installing nltk, then go to Python3.6 shell. In shell, use: import ultk, then use: ultk.download('all')

after finish above steps, you could start next part - running this application.

# Usage
When you finish the environment configuration, you could start follow thos steps below to run this application:

- first, run: python3.6 manage.py makemigrations system    and   python3.6 manage.py migrate system  to build the database.
- second, run: python3.6 manage.py importdata company  and   python3.6 manage.py importdata people  to import all data from json files to mysql database.
- third, change path to system folder and then run: python3.6 ../manage.py test system   to test this application
- last, you could setup web server and browe the webpage and input argument from webpage and see the results returned.
