# Description


## Actions

### Load data
```
python manage.py load_json --docname comments
```
```
python manage.py load_json --docname posts
```

### Run tests
For tests defaul unittests package is used. To run test execute command:
```
python manage.py test;
```
```
python manage.py test master_system.test.test_posts_api
```
```
python manage.py test master_system.test.test_comments_api
```

### Docker commands
```
docker build -t fakeapi_service .
```
```
docker run --name fakeapi_service_container --rm -p 8000:8000 fakeapi_service
```
###### Staying in info folder: 
```
docker-compose up -d
```
```
docker-compose build --no-cache && docker-compose up -d
```
```
docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec backend python manage.py migrate
```
```
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
```
```
docker-compose exec backend python manage.py load_json_data posts
```
```
docker-compose exec backend python manage.py load_json_data comments
```

### Links
1. http://127.0.0.1/swagger/
2. http://127.0.0.1/admin/


### Limitations and assumptions

1. No restrictions to change other user's content as it was defined in the original task: "The user_id for the new posts created is always 99999942 since we don’t implement the user model.".
2. CRUD operations are GET, POST, PUT, PATCH, DELETE
3. No need for Nginx and gunicorn
4. DEBUG to True to see errors
5. makemigrations is paro of CI/CD pipeline

## Tasks

1. env done 
2. packages
3. define models
4. load data
5. define endpoints
    5.1. serializers
    5.2. view 
    5.3. documentation
    5.4. pagination
    5.5. permisions
    5.6. tokens
    5.7. search/filter (?) 
6. configure servier
6.1. with gunocor, allowed hosts in settings
6.2. move keys to another (dedicated) file
7. tests
8. dockerise

## Task description
 
Create a simple REST API to interact with the Fake API in JSONPlaceholder - Free Fake REST API
- [x] Create a Django command to import the data for the first time (posts and comments only) from JsonPlaceholder Free Fake Rest API to the local Postgres.
- [ ] Finish all endpoint in master system
- [ ] Finish all tests in master system
- [ ] Add Postgres in a separate Docker container
You can define whatever you want in your local database
Create a Rest API to manage that data in those models.
- [ ] Implement all CRUD (POST, GET, PUT/PATCH/DELETE) operations.
- [ ] CORS
- [ ] Secrets into env file
- [x] The user_id for the new posts created is always 99999942 since we don’t implement the user model.
- [x] Provide users authentication and request authorization through Bearer Token.
- [ ] Synchronize both systems. The system you are implementing is the MASTER. You can decide how and when this synchronization will be done. 
- [ ] Please write a README to specify how it can be triggered.
- [ ] We prefer a tested and well documented task than a quick one.
- [ ] Deliver the task using Docker and docker-compose.
- [ ] Write test for custom management command 
- [ ] hide secret key
- [ ] add db.sqlite3 to .dockerignore

Notes You can resort to use any library that you need but specify the purpose of including it.