# -*- coding: utf-8 -*-
# Библа для обращения к кинопоиску
import requests
import bot_info
import json
import random



def get_film_to_genres(genres):
    a = 0
    while a < 1:
        try:
            genres_id = bot_info.genres_id[genres]
            rand_page = random.randint(1,2)
            rand_item = random.randint(0,19)
            # получение фильмов с выбранным жанром
            url_film_to_genres = f'https://kinopoiskapiunofficial.tech/api/v2.2/films?genres={genres_id}&page={rand_page}'
            # Запрос на API кинопоиска
            film_list = requests.get(url_film_to_genres, headers={'X-API-KEY': "0abebfe7-7e3b-41ac-94e6-95525f0b018f"})
            # Получили список фильмов сделав словарем для дальнейшей работы
            body = json.loads(film_list.text)
            films = body['items']
            # Выбрали случайный фильм из списка
            film = films[rand_item]
            # Получаем картинки с филма
            images_url = get_image_film_to_id(film["kinopoiskId"])
            # Проверка на наличие картинок
            if images_url != False:
                return [film["kinopoiskId"], film["nameOriginal"], film["nameRu"], images_url, genres]
        except Exception as ex:
            a += 1
            print(f"Error, no film found. Try again, {ex}")

def get_image_film_to_id(id):
    try:
        # получение картинок выьранного фильма
        url_film_to_genres = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}/images'
        # Запрос на API кинопоиска
        # Может не быть картинок поэтому проверяем
        image_list = requests.get(url_film_to_genres, headers={'X-API-KEY': "0abebfe7-7e3b-41ac-94e6-95525f0b018f"})

        # Получили список картинок сделав словарем для дальнейшей работы
        body = json.loads(image_list.text)
        images = body['items']
        # Добавил описание фильма если есть
        url_film_to_id = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'
        # Запрос на API кинопоиска
        film = requests.get(url_film_to_id, headers={'X-API-KEY': "0abebfe7-7e3b-41ac-94e6-95525f0b018f"})
        # Сделали словарем
        film = json.loads(film.text)
        # добавили описание
        if film['description'] is not None:
            description = film['description']
        else:
            description = "Нет Описания"
        # Проверим наличие 3 картинок  фильме
        if len(images) < 2:
            return False
        # Сохраним ссыдки
        images_url = [images[0]['imageUrl'], images[1]['imageUrl'], images[2]['imageUrl'], description]
        return images_url
    except:
            print("Error, no images found. Try again")
            return False

def get_recommendation_to_genres(genres):
    while True:
        genres_id = bot_info.genres_id[genres]
        # получение фильмов с выбранным жанром сортированые по рейтингу
        url_film_to_genres = f'https://kinopoiskapiunofficial.tech/api/v2.2/films?genres={genres_id}&order=RATING&page=1'
        # Запрос на API кинопоиска
        film_list = requests.get(url_film_to_genres, headers={'X-API-KEY': "0abebfe7-7e3b-41ac-94e6-95525f0b018f"})

        # Получили список фильмов сделав словарем для дальнейшей работы
        body = json.loads(film_list.text)
        films = body['items']
        # Формируем список с ссылками на фильмы
        film_url_list = []
        for i in range(5):
            # Ищем фильм по id 
            id = films[i]['kinopoiskId']
            url_film_to_genres = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'
            # Запрос на API кинопоиска
            film = requests.get(url_film_to_genres, headers={'X-API-KEY': "0abebfe7-7e3b-41ac-94e6-95525f0b018f"})
            # Сделали словарем
            film = json.loads(film.text)
            # добавили ссылку на фильм в список
            film_url_list.append(film['webUrl'])
        # Отправили список фильмов
        return film_url_list

#get_recommendation_to_genres("фантастика")