# -*- coding: utf-8 -*-
from mysql.connector import MySQLConnection
from mysql.connector import Error
import bot_info

from configparser import ConfigParser
import bot_info

# Функция записи выбора пользователя по жанру
def send_info_to_db(user_id, genres, rating, film = "sd"):
    # Собираем параметры для хранимой процедуры 
    argx = (user_id, genres, rating, film)
    # Параметры функции: Название хранимой процедуры и пареметры самой хранимки
    res = execute_query('add_user_rating', argx)
    return res

# Функция просмотра всех выборов пользователя
def get_info_to_db(user_id):
    # Тут запятая потому что картежи так работают если 1 параметр
    argx = (user_id,)
    # Получаем данные
    res = execute_query('get_user_rating', argx)
    # Разбираем их на составляющие
    for user_ratings in res:
        user_rating = user_ratings.fetchall()
    return user_rating

def get_flag_to_db(user_id):
    # Тут запятая потому что картежи так работают если 1 параметр
    argx = (user_id,)
    # Получаем данные
    res = execute_query('get_user_rating', argx)
    # Разбираем их на составляющие
    for user_ratings in res:
        user_rating = user_ratings.fetchall()
    # Проверяем на количество полученых сообщений если кратно 10 то заканчиваем и выводим рекомендацию
    if len(user_rating) % 10 == 0:
        return False
    else:
        return True


# Сборшик конфига базы для интерпритации библиотекой
def read_db_config(filename=f'{bot_info.config}', section='mysql'):
    # Парсим и читаем ini файл
    parser = ConfigParser()
    parser.read(filename)
 
    # Собираем данные в формат запроса
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

# Проверка подключения
def _connection():
    db_config = read_db_config()
    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        conn.close()
        print('Connection closed.')

    return conn

# Отправка запроса через хранимую процедуру которая лежит в базе. Так удобнее и безопаснее
def execute_query(exec_name, argx = None):
    try:
        # Проверяем кофиг и подключаемся к базе
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        # Вызываем хранимую процедуру
        if argx == None:
            cursor.callproc(exec_name)
        else:
            cursor.callproc(exec_name, argx)
        conn.commit()
        return cursor.stored_results()
    except Error as e:
        return(f"error '{e}' occurred")
    
    finally:
        cursor.close()
        conn.close()

#_connection()

