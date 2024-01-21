# Базовый образ
FROM python:3.11

# Установка зависимостей проекта
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование исходного кода проекта
COPY . /app/

# Переход в папку с manage.py
WORKDIR /app/multidor

# Сборка статических файлов
RUN python manage.py collectstatic --noinput --clear

# Порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
