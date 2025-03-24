from flask import Flask, render_template 
import os 
import psycopg2  

app = Flask(__name__)  

def get_db_connection(): 
    host = os.getenv('DATABASE_HOST', 'localhost')  # Получаем значение  переменной окружения DATABASE_HOST 
    dbname = os.getenv('POSTGRES_DB', 'mydatabase') # Получаем значение  переменной окружения POSTGRES_DB 
    user = os.getenv('POSTGRES_USER', 'myuser')     # Получаем значение переменной окружения POSTGRES_USER 
    password = os.getenv('POSTGRES_PASSWORD', 'mypassword') # Получаем значение переменной окружения POSTGRES_PASSWORD  
    conn = psycopg2.connect(dbname=dbname, 
                            user=user, 
                            password=password, 
                            host=host) 
    return conn  

@app.route('/') 
def hello_world(): 
    conn = get_db_connection() 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM messages") 
    messages = cursor.fetchall() 
    cursor.close() 
    conn.close() 
    return render_template('index.html', messages=messages)  

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')