# Backend REST API
## Installation
```
git clone https://github.com/yduan004/REST_API.git
pip install -r requirements.txt
python app.py
```

## Description
This is a REST API implemented using Flask and popular extension Flask-RESTful. It allows users register and log in, as well as create stores and items with authentication. It can be modified to be a REST API for any type of applications such as managing lab protocals with CRUD operations. 

The resources are stored in SQLite database by using SQLAlchemy. Postman can be used to do automated testing of the API by writing pre-request scripts and test scripts and running the ordred requests/workflow. It also added abuse prevention and manage user logout by using JWT blocklist to revoke access token.

## Deployment
### On Heroku
This API service is deployed on Heroku at [https://rest-api-s.herokuapp.com/](https://rest-api-s.herokuapp.com/). Use Postman to test the API. The supported endpoints are `GET /items`, `GET /stores`, `POST /login`, `POST /register`, `GET /user/<user_id>`, `DEL /user/<user_id>`, `GET /item/<name>`, `GET /store/<name>`, `POST /item/<name>`, `POST /store/<name>`, `PUT /item/<name>`, `DEL /item/<name>`, `DEL /store/<name>`.

### Run as Docker Image
```
docker run -p 5000:5000 yuzhu2/rest_api
```
