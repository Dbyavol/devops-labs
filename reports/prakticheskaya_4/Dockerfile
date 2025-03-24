# Используем базовый образ Python 
FROM python:3.9  
# Устанавливаем psycopg2 для подключения к PostgreSQL 
RUN pip install psycopg2-binary Flask  
# Копируем все файлы в контейнер 
COPY . /app
WORKDIR /app 

# Определяем команду для запуска приложения 
CMD ["python", "app.py"]
