# -*- coding: utf-8 -*-
# Импорты для работы бота
from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import types
import asyncio

import numpy as np

# Токен из файла с данными 
import bot_info 
# Функции из другого документа для работы с кинопоиском
from kinopoisk import get_film_to_genres
from kinopoisk import get_recommendation_to_genres
# Функции для работы с базой 
from send_db import send_info_to_db
from send_db import get_flag_to_db
# Функция адаптации
from adaptation import genres_adaptation
# Лучший жанр для пользователя
from adaptation import get_max_genres
# Получаем бота для работы
bot = AsyncTeleBot(bot_info.TOKEN)



# Обработчик событий старотовых команд
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Этот бот был создн для анализа ваших жанровых предпочтений в фильмах. \n
Для начала работы напишите команду /recommendation.
""")

# Обработчик старта логики бота
@bot.message_handler(commands=['recommendation'])
async def start_rec(message):
    await bot.reply_to(message, """
Сейчас вам будет предложены издобраения из фильмов и вам нужно оценить их по 10 бальной шкале.
Далее мы определим какие еще фильмы вам могли бы понравиться.
""")
    # Выбор 1 случайного жанра
    genres = np.random.choice(list(bot_info.genres_rating))
    await send_question(message.from_user.id, genres)

# Обработчик случайных сообщений
@bot.message_handler(content_types=['text'])
async def all_message(message):
    await bot.reply_to(message, '''Я пока не понимаю слов. Воспользуйтесь командами:
/start (/help) для получения информации 
или 
/recommendation для началы работы бота
''')

# Обрабатывает любые кнопи из чата
@bot.callback_query_handler(func=lambda call: True)
async def callback_worker(call):
    # Разделения данных на рейтинг и жанр и фильм
    value = call.data.split('.')
    rating, genres, film = value[0], value[1], value[2]
    # Запись результатов в БД
    send_info_to_db(call.from_user.id, genres, rating, film)
    # Логика обработки
    # Функция обработки e-greedy алгоритм
    genres = genres_adaptation(rating, call.from_user.id)
    # Сообщаем пользователю что оценка поставлена
    await bot.answer_callback_query(call.id, text="Оценка поставлена")
    # Обновляем сообщение что бы убрать кнопки, избегаем повторного нажатия и сообщить о выборе пользователя
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Ваша оценка данному фульму: {rating}')

    # Проверка на количество вопросов
    flag = get_flag_to_db(call.from_user.id)
    # Отправка нового запроса
    if flag:
        await send_question(call.message.chat.id, genres)
    else:
        await send_recommendation(call.message.chat.id, call.from_user.id)

# Оправка вопросов message_id не всегла используется пожтому None
async def send_question(chat_id, genres):
    # Получаем набор параметров необходимых для вопроса
    data = get_film_to_genres(genres)
    #data[0] -> id фильма
    #data[1] -> Оригинальное название
    #data[2] -> Название на русском
    #data[3] -> Набор картинок
    #data[4] -> Жанр фильма
    # Определим доступные кнопки
    keyboard = types.InlineKeyboardMarkup(); # клавиатура
    # Такая незаурядная callback_data потому что лучше возможности для передачи в обработчик жанра я не придумал
    key_1 = types.InlineKeyboardButton(text='1', callback_data=f'1.{genres}.{data[1]}')
    key_2= types.InlineKeyboardButton(text='2', callback_data=f'2.{genres}.{data[1]}')
    key_3= types.InlineKeyboardButton(text='3',  callback_data=f'3.{genres}.{data[1]}')
    key_4 = types.InlineKeyboardButton(text='4', callback_data=f'4.{genres}.{data[1]}')
    key_5= types.InlineKeyboardButton(text='5', callback_data=f'5.{genres}.{data[1]}')
    key_6= types.InlineKeyboardButton(text='6', callback_data=f'6.{genres}.{data[1]}')
    key_7 = types.InlineKeyboardButton(text='7', callback_data=f'7.{genres}.{data[1]}')
    key_8= types.InlineKeyboardButton(text='8', callback_data=f'8.{genres}.{data[1]}')
    key_9= types.InlineKeyboardButton(text='9', callback_data=f'9.{genres}.{data[1]}')
    key_10 = types.InlineKeyboardButton(text='10', callback_data=f'10.{genres}.{data[1]}')
    keyboard.add(key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10)
    # Определи вопрос
    question = 'Тебе приглянулся фильм?? Пожалуйста оцени его по 10 бальной шкале. После этого мы попытаемся подстроиться под твой вкус.'

    # Отправим сообщение
    await bot.send_message(chat_id, f'Фильм: {data[1]}({data[2]}), Жанр: {data[4]}')
    await bot.send_photo(chat_id, photo=data[3][0])
    await bot.send_photo(chat_id, photo=data[3][1])
    await bot.send_photo(chat_id, photo=data[3][2])
    await bot.send_message(chat_id, text=question, reply_markup=keyboard)

# Оправка рекомендации
async def send_recommendation(chat_id, user_id):
    genres = get_max_genres(user_id)
    data = get_recommendation_to_genres(genres)
    await bot.send_message(chat_id, f'Вам больше подходит жанр {genres}. \n Мы рекомендуем вам посмотреть следующие фильмы: \n {data[0]} \n {data[1]} \n {data[2]} \n {data[3]} \n {data[4]}')


# Запускаем бота
asyncio.run(bot.polling(none_stop=True))
