# Backend REST API
## Installation
```

pip install -r requirements.txt
python app.py
```

## Description
This project is implemented using Flask, and is a REST API for a store with authentication. It can be modified to be a REST API for any type of applications such as managing lab protocals with CRUD operations. 

The resources are stored in SQLite database by using SQLAlchemy. Postman can be used to do automated testing of the API by writing test script and run the workflow. It also added abuse prevention by using JWT blocklist.

## Deployment
### On Heroku
This API service is deployed on Heroku at [https://rest-api-s.herokuapp.com/](https://rest-api-s.herokuapp.com/). Use Postman to test the API. The supported endpoints are `GET /items`, `GET /stores`, `POST /login`, `POST /register`, `GET /item/<name>`, `GET /store/<name>`, `POST /item/<name>`, `POST /store/<name>`, `PUT /item/<name>`, `DEL /item/<name>`, `DEL /store/<name>`.

### Run as Docker Image
```
docker run -p 5000:5000 yuzhu2/rest_api
```
