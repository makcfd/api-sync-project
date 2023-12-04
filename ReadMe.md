[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

# Description
RESTful API service built using Django and Django REST framework, designed to interact with the JSONPlaceholder (https://jsonplaceholder.typicode.com/). It primarily focuses on posts and comments data. This project includes a Django command for initial data import from JSONPlaceholder to a local PostgreSQL database and provides CRUD operations on the data. It features user authentication, request authorization via Bearer Token, and a synchronization mechanism where the local system acts as the MASTER. The data synchronization is executed instantly and automatically after changes have been applied to the master system. The results of synchronization is avaliable at POST, PUT, PATCH, DELETE endpoints as a response attribute with the response code received from jsonplaceholder service.

## Prepare the implementation
- Clone repo:
```
git clone git@github.com:makcfd/sync-api-project.git
```
- Go to the infra folder:
```
cd api-sync-project/infra
```
- Build the services
```
docker-compose build --no-cache && docker-compose up -d
```
- Prepare the backend
```
docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec backend python manage.py migrate
```
```
docker-compose exec backend python manage.py createsuperuser --noinput
```
- Load data
```
docker-compose exec backend python manage.py load_json_data posts
```
```
docker-compose exec backend python manage.py load_json_data comments
```
### Run tests
For tests defaul unittests package is used. To run test execute command:
```
docker-compose exec backend python manage.py test;
```
```
docker-compose exec backend python manage.py test master_system.test.test_posts_api
```
```
docker-compose exec backend python manage.py test master_system.test.test_comments_api
```

### cUrl examples
- Get Bearer token
```
curl -X POST http://127.0.0.1:8000/api/auth/jwt/create \
   -H 'Content-Type: application/json' \
   -d '{"username":"admin","password":"admin"}'
```
-Get posts:
```
curl -X GET http://127.0.0.1:8000/api/v1/posts/ -H 'Authorization: Bearer <YOUR TOKEN>'
```
- Create a new post:
```
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
   -H 'Content-Type: application/json' \
   -H 'Authorization: Bearer <YOUR TOKEN>' \
   -d '{"title": "foo","body": "bar"}'
```

### Links
1. Project documentation available at the address: http://127.0.0.1/swagger/
2. Admin panel is available at the address: http://127.0.0.1/admin/


# Limitations and assumptions

1. No restrictions to change other user's content as it was defined in the original task: "The user_id for the new posts created is always 99999942 since we don’t implement the user model.".
2. CRUD operations are GET, POST, PUT, PATCH, DELETE
3. No need for Nginx and gunicorn
4. DEBUG to True to see errors
5. It is expected that "makemigrations" and "migrate" commands are part of CI/CD pipeline

# Libraries Used
- Django REST Framework: For creating RESTful APIs.
- Django REST Framework SimpleJWT: For JWT-based authentication.
- Requests: For making HTTP requests to JSONPlaceholder API.
- Psycopg2: PostgreSQL database adapter for Python.