# -*- coding: utf-8 -*-

import numpy as np
from send_db import get_info_to_db
import bot_info

# Функция адаптации вопросов
def genres_adaptation(rating, user_id):
    # на основе оценки выберем вероятность изменения жанра
    # если оценка 1 то 100 %
    # если оценка 2 то 90 %
    # итд...
    # если оценка 10 то 10 %
    e = 1.1 - 0.1 * float(rating)
    # Выберем на основе нормального распределения меняем ли жанр или выбираем максимальный
    if np.random.rand() < e:
        # Попались на изменение выбераем случайный жанр
        return np.random.choice(list(bot_info.genres_rating))
    # Не попались вызваем функцию поиска максимального жарна
    genres = get_max_genres(user_id)
    return genres
    
    

 
def get_max_genres(user_id):
    # копируем изначальную конфигурацию словаря
    genres_rating = bot_info.genres_rating.copy()
    # Вытащим с базы все выборы пользователя
    user_rating = get_info_to_db(user_id)
    # rating[0] -> use_id
    # rating[1] -> жанр
    # rating[2] -> оценка
    #genres_rating['Жанр'][0] -> сумма оценк
    #genres_rating['Жанр'][1] -> Количество оценок
    for rating in user_rating:
        # заполним масив с данными 
        genres_rating[rating[1]][0] += rating[2]
        genres_rating[rating[1]][1] += 1
    # Находим максимальню оценку
    # начальные нулевые значения
    max_rating = 0.0
    genres = ''
    for key, value in genres_rating.items():
        # Проверка на 0
        if value[1] != 0:
            # Если значение больше то меняем
            if max_rating < value[0]/value[1]:
                max_rating = value[0]/value[1]
                genres = key
    return genres