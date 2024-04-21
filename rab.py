from telebot import *
import pytube
import os
import requests
import re
from moviepy.editor import VideoFileClip

bot = telebot.TeleBot('6273204407:AAHc-578ru2Uie1JQnypi7YjdXL3fUU2-ew')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("help")
    btn2 = types.KeyboardButton("Конвертор видео")
    btn3 = types.KeyboardButton("Скачивание видео со сторонних ресурсов")
    btn4 = types.KeyboardButton("Скачивание фото и документов со сторонних ресурсов")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, f"Привет {message.from_user.username}! Я бот. Вот мои функции",
                     reply_markup=markup)

youtube = False
tiktok = False
fail = False


@bot.message_handler(content_types=['text'])
def choose(message):
    global youtube, tiktok, fail
    if message.text == 'help':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сколько времени')
        btn2 = types.KeyboardButton('Цель проекта')
        btn3 = types.KeyboardButton('Вернуться')
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)

    elif message.text == 'Сколько времени':
        current_time = datetime.now().strftime('%H:%M:%S')
        bot.send_message(message.chat.id, current_time)

    elif message.text == 'Цель проекта':
        bot.send_message(message.chat.id, text='''Проект представляет из себя бота, который даёт пользователю возможности:
        1. Скачивание видео со сторонних ресурсов (YouTube, TikTok, Pinterest);
        2. Конвертация видео в любые форматы;
        3. Скачивание любых других данных со сторонних ресурсов (фото, документы и т.д.).
                                            ''')

    elif message.text == 'Скачивание видео со сторонних ресурсов':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('YouTube')
        btn2 = types.KeyboardButton('TikTok')
        btn3 = types.KeyboardButton('Вернуться')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)

    elif message.text == 'YouTube':
        youtube = True
        tiktok = False
        bot.send_message(message.chat.id, text="пришлите пожалуйста ссылку в формате "
                                               "https://www.youtube.com/watch...",
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'TikTok':
        tiktok = True
        youtube = False
        bot.send_message(message.chat.id, text="пришлите пожалуйста ссылку в формате "
                                               "https://www.tiktok.com/",
                         reply_markup=types.ReplyKeyboardRemove())

    elif youtube:
        downld_youtube(message)

    elif tiktok:
        downld_tiktok(message)

    elif fail:
        down_fail(message)

    elif message.text == 'Скачивание фото и документов со сторонних ресурсов':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Скачивание фото')
        btn2 = types.KeyboardButton('Скачивание документов')
        btn3 = types.KeyboardButton('Вернуться')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)

    elif message.text == 'Скачивание фото':
        fail = True
        bot.send_message(message.chat.id, text="Введите ссылку на файл для скачивания: ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Скачивание документов':
        fail = True
        bot.send_message(message.chat.id, text="Введите ссылку на файл для скачивания: ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Вернуться':
        start(message)


@bot.message_handler(content_types=['text'])
def downld_youtube(message):
    ytlink = message.text
    if str(ytlink).startswith('https://www.youtube.com/watch'):
        bot.send_message(message.chat.id, 'видео загружается, подождите пожалуйста...')
        try:
            youtubelink = pytube.YouTube(ytlink)
            video = youtubelink.streams.get_highest_resolution()
            if os.path.exists('res.mp4'):
                os.remove('res.mp4')
            out_file = video.download(filename='res')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp4'
            os.rename(out_file, new_file)
            vd = open('res.mp4', 'rb')
            bot.send_video(message.chat.id, vd)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'видео успешно загружено!', reply_markup=markup)
        except Exception as e:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'ошибка при загрузке видео, попробуйте еще раз', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вернуться")
        markup.add(btn1)
        if message.text == 'Вернуться':
            start(message)


def get_tiktok_video_id(url):
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)


@bot.message_handler(content_types=['text'])
def downld_tiktok(message):
    if str(message.text).startswith('https://www.tiktok.com/'):
        if os.path.exists('tiktok.mp4'):
            os.remove('tiktok.mp4')
        response = requests.get(message.text)
        video_id = get_tiktok_video_id(response.url)
        response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')

        if response.status_code == 200:
            with open(f"tiktok.mp4", "wb") as file:
                file.write(response.content)
            vd = open('tiktok.mp4', 'rb')
            bot.send_video(message.chat.id, vd)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'видео успешно загружено!', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'ошибка при загрузке видео, попробуйте еще раз', reply_markup=markup)

    elif message.text == 'Вернуться':
        start(message)


def down_fail(message):
    if message.text == 'Вернуться':
        start(message)
    else:
        user_input = message.text
        filename = user_input.split('/')[-1]
        r = requests.get(user_input, allow_redirects=True)
        open(filename, "wb").write(r.content)
        bot.send_document(message.chat.id, open(filename, 'rb'))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


bot.polling()