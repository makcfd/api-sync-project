FROM python:3.9-slim
RUN pip install --upgrade pip
WORKDIR /app
COPY fakeapi/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY fakeapi/ .
CMD ["python", "manage.py", "runserver", "0:8000"] 

#CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]