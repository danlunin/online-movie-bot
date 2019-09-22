# -*- coding: utf-8 -*-
import telebot
from google_scraper import get_english_name_google, extract_link_watch
from language_utils import is_english
from imdb import get_imdb_data, parse_imdb_data
from telegram_markup_maker import prepare_pretty_data, prepare_link
from telebot import types
import os

WELCOME_MESSAGE = "Hello, I'm a movie bot. Just send me a film name and I'll" \
                  " try to provide all data "\
                          "about it. Also I'll try to find a link for" \
                  " watching it."
ERROR_MESSAGE = 'Try other name again.'
EXCEPTION_MESSAGE = 'Sorry, an exception occurred.'
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/Get help', '/Помощь')
    msg = bot.reply_to(message, 'Hello', reply_markup=markup)
    bot.register_next_step_handler(msg, send_help)

    bot.reply_to(message, WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def send_help(message):
    if message.text == '/Помощь':
        bot.reply_to(message, 'Пришлите название фильма на русском '
                              'или на английском.'
                              ' Если вы пришлёте название на русском, то бот '
                              'найдёт перевод на кинопоиске '
                              'и пришлёт информацию с IMDb. ')
    else:
        bot.reply_to(message, 'Just send movie name in russian or in english.'
                              ' If you send it in russian the bot will check '
                              'a translation on Kinopoisk and will find'
                              'the movie on IMDb.')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        if message.text == '/Помощь':
            send_help(message)
            return
        elif message.text == '/Get help':
            send_help(message)
        markdown_message = handle_movie_query(message)
        bot.reply_to(message, markdown_message, parse_mode='Markdown')
        with open("queries.txt", "a") as file:
            file.write("Query: " +
                       message.text + " Sender: " +
                       message.chat.username + '\n')
    except Exception as e:
        print(e)
        bot.reply_to(message, EXCEPTION_MESSAGE)


def handle_movie_query(message):
    query = get_english_name_google(message.text) \
        if not is_english(message.text) else message.text
    print(query)
    if query is not None:
        imdb_data = get_imdb_data(query)
        print(imdb_data)
        data = parse_imdb_data(imdb_data)
        pretty_data = prepare_pretty_data(data)
        bot.reply_to(message, pretty_data, parse_mode='Markdown')
        link = extract_link_watch(message.text)
        markdown_message = prepare_link(link)
    else:
        markdown_message = ERROR_MESSAGE
    return markdown_message


if __name__ == '__main__':
    bot.polling(timeout=123)
