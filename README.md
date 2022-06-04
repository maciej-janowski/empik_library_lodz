# EmpikGo codes sharing API

## Assumption of the project
Libraries in my city share the codes for E-Books platform w ith people that are users of the libraries and have a personal library card. But these codes are shared by giving people a slip of paper with a code on it (and instruction on how to further proceed to get the access). I thought that maybe there could be an option to create an API which would make this process more digital. That's how I came up with an idea to create an API for this purpose

![title](empik_api_screenshots/empik_code_example.jpg)

## Description of how API works
* There are three user account types: empik, library and user
* Each user type has its own functions and paths

* Authorization is not required for creation of users but all other routes are secured and require token authentication
* In order to log in - user need to enter email and password. Also scope needs to be indicated as this will allow access to relevant endpoints (token will be generated)

![title](empik_api_screenshots/email_password.jpg)

![title](empik_api_screenshots/scopes.jpg)


### Empik

* Empik user can send codes which will be available for users in csv file. All codes sent will be saved in the database

![title](empik_api_screenshots/empik_send_codes.jpg)

* Empik user can check the statuses of codes (if they were used or not)

![title](empik_api_screenshots/empik_check_codes.jpg)


### Reader/Library user

* Reader/person using library can request a code

![title](empik_api_screenshots/user_request_code.jpg)

* He/She can also check if raised request is still processed or it is closed

![title](empik_api_screenshots/user_request_status.jpg)


### Library

* Library can check all requests that were are to it

![title](empik_api_screenshots/library_stats.jpg)

* Library can verify the request and either accept it or reject it

![title](empik_api_screenshots/library_verify_request.jpg)

* Library can see in which request codes were assigned and which ones 

![title](empik_api_screenshots/library_codes_assigned.jpg)



## Technologies
* Python (FastAPI, SQLAlchemy, pandas)
* JWT

