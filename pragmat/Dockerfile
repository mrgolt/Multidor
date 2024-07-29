# Базовый образ
FROM python:3.11

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app/

WORKDIR /app/

RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
