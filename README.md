## Flask Code Sample
This project was created in order to show programming skills of Python/Flask developers from Jelvix.

### Task:
Create API for managing tradings with Google authentication.

### Tools:
Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful-Swagger, Flask-API, GoogleAPI OAuth2, 

To authorize go to and after google authentication copy the access token:  
http://localhost:9000/authorize
![Authorise demonstration](/readme/flask-login.gif)  
 
You can see the docs on:
http://0.0.0.0:9000/api/spec.html#!/spec/  
![Authorise demonstration](/readme/flask-docs.gif)  


#### For code demonstration:
- clone this repository;
- open directory with project in the terminal;
- open directory "src" `cd src`;
- run command `docker-compose up --build`;
- after this go to the chosen link.  
 
The first registered user will be with access to exchanges, logbook & user management.  
#### Note: FOR CODE DEMONSTRATION ONLY.