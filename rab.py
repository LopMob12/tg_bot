from telebot import *
import pytube
import requests
import re
from moviepy.editor import *

bot = telebot.TeleBot('6852294591:AAGbTddCmXkAa7k4UsdktKKhMvg52UWtt8M')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Дополнительные Данные")
    btn2 = types.KeyboardButton("Конвертор видео")
    btn3 = types.KeyboardButton("Скачивание видео со сторонних ресурсов")
    btn4 = types.KeyboardButton("Скачивание фото, аудио и документов со сторонних ресурсов")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, f"Привет {message.from_user.username}! Я бот. Вот мои функции",
                     reply_markup=markup)


youtube = False
tiktok = False
fail = False
audio = False
youtube_music = False
lnk = ''
qwl = False


@bot.message_handler(content_types=['text'])
def choose(message):
    global youtube, tiktok, fail, audio, youtube_music
    if message.text == 'Дополнительные Данные':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Сколько времени', 'Цель проекта', 'Вернуться')

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
        markup.add('YouTube', 'TikTok', 'Вернуться')
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

    elif youtube and not qwl:
        choose_quality(message)

    elif youtube and qwl:
        downld_youtube(message)

    elif tiktok:
        downld_tiktok(message)

    elif fail:
        down_fail(message)

    elif audio:
        down_audio(message)

    elif youtube_music:
        down_music(message)

    elif message.text == 'Скачивание фото, аудио и документов со сторонних ресурсов':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Скачивание фото', 'Скачивание документов', 'Скачивание аудио', 'Скачивание музыки с ютуба', 'Вернуться')
        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)

    elif message.text == 'Скачивание фото':
        fail = True
        bot.send_message(message.chat.id, text="Введите ссылку на файл для скачивания: ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Скачивание документов':
        fail = True
        bot.send_message(message.chat.id, text="Введите ссылку на файл для скачивания: ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Скачивание аудио':
        audio = True
        bot.send_message(message.chat.id, text="Введите ссылку на файл для скачивания(Длительность аудио по времени не должна превышать 5 минут): ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Скачивание музыки с ютуба':
        youtube_music = True
        bot.send_message(message.chat.id, text="Введите ссылку на видео для скачивания песни: ",
                         reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Конвертор видео':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('MP3', 'AVI', 'MKV')
        bot.send_message(message.chat.id, text="Выберите формат в который хотите конвертировать видео",
                         reply_markup=markup)
    elif message.text == 'MP3':
        bot.send_message(message.chat.id, text="Пришлите видео", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, konvertorr_MP)
    elif message.text == 'AVI':
        bot.send_message(message.chat.id, text="Пришлите видео", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, konvertorr_AV)
    elif message.text == 'MKV':
        bot.send_message(message.chat.id, text="Пришлите видео", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, konvertorr_MKV)
    elif message.text == 'Вернуться':
        start(message)


@bot.message_handler(content_types=['text'])
def choose_quality(message):
    global lnk, qwl
    qwl = True
    lnk = message.text
    btn1 = types.KeyboardButton('144p')
    btn2 = types.KeyboardButton('240p')
    btn3 = types.KeyboardButton('360p')
    btn4 = types.KeyboardButton('720p')
    btn5 = types.KeyboardButton('1080p')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, text="Выберите качество видео", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def downld_youtube(message):
    global youtube, qwl
    ytlink = lnk
    quality = message.text
    if str(ytlink).startswith('https://www.youtube.com/watch'):
        bot.send_message(message.chat.id, 'видео загружается, подождите пожалуйста...',
                         reply_markup=types.ReplyKeyboardRemove())
        try:
            youtubelink = pytube.YouTube(ytlink)
            stream = youtubelink.streams
            video = stream.filter(res=quality).desc().first()
            if os.path.exists('res.mp4'):
                os.remove('res.mp4')
            if os.path.exists('audio.mp3'):
                os.remove('audio.mp3')
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
            video.download(filename='video.mp4')
            audio = stream.filter(adaptive=True, only_audio=True).desc().first()
            audio.download(filename='audio.mp3')
            video_clip = VideoFileClip('video.mp4')
            audio_clip = AudioFileClip('audio.mp3')
            video_clip_with_audio = video_clip.set_audio(audio_clip)
            video_clip_with_audio.write_videofile("res.mp4")
            vd = open('res.mp4', 'rb')
            bot.send_video(message.chat.id, vd, timeout=10000)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'видео успешно загружено!', reply_markup=markup)
            youtube = False
            qwl = False
        except Exception:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вернуться")
            markup.add(btn1)
            bot.send_message(message.chat.id, 'ошибка при загрузке видео, попробуйте еще раз', reply_markup=markup)
            youtube = False
            qwl = False


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


def down_audio(message):
    if message.text == 'Вернуться':
        start(message)
    else:
        user_input = message.text
        filename = user_input.split('/')[-1]
        r = requests.get(user_input, stream=True)
        open(filename, "wb").write(r.content)
        bot.send_audio(message.chat.id, open(filename, 'rb'))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


def down_music(message):
    if message.text == 'Вернуться':
        start(message)
    else:
        user_input = message.text
        yt = pytube.YouTube(user_input, use_oauth=True)
        stream = yt.streams.get_by_itag(251)
        f = open(stream.download(), 'rb')
        bot.send_document(message.chat.id, f)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


def konvertorr_MP(message):
    try:
        if message.text == 'Вернуться':
            start(message)
        else:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('video.mp4', 'wb') as video_file:
                video_file.write(downloaded_file)
            video_clip = VideoFileClip('video.mp4')
            audio_clip = video_clip.audio
            audio_clip.write_audiofile("audio.mp3")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Вернуться')
            markup.add(btn1)
            audio_file = open("audio.mp3", "rb")
            bot.send_audio(message.chat.id, audio_file)
            bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id,
                         text="Произошла ошибка при конвертации видео в "
                              "аудио. Пожалуйста, попробуйте еще раз или обратитесь к администратору.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


def konvertorr_AV(message):
    try:
        if message.text == 'Вернуться':
            start(message)
        else:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('video.mp4', 'wb') as video:
                video.write(downloaded_file)
            clip = VideoFileClip("video.mp4")
            clip.write_videofile("video.avi", codec='mpeg4', fps=144, bitrate='5000k')
            with open("video.avi", "rb") as video_file:
                bot.send_video(message.chat.id, video_file)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Вернуться')
            markup.add(btn1)
            bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id,
                         text="Произошла ошибка при конвертации видео. "
                              "Пожалуйста, попробуйте еще раз или обратитесь к администратору.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


def konvertorr_MKV(message):
    try:
        if message.text == 'Вернуться':
            start(message)
        else:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('video.mp4', 'wb') as video:
                video.write(downloaded_file)

            clip = VideoFileClip("video.mp4")
            clip.write_videofile("video.mkv", codec='libx264')

            if os.path.isfile("video.mkv"):
                with open("video.mkv", "rb") as video_file:
                    bot.send_video(message.chat.id, video=video_file)
                os.remove("video.mp4")
                os.remove("video.mkv")
            else:
                bot.send_message(message.chat.id, text="Произошла ошибка при конвертации видео.")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Вернуться')
            markup.add(btn1)
            bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id,
                         text="Произошла ошибка при конвертации видео."
                              " Пожалуйста, попробуйте еще раз или обратитесь к администратору.")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)


bot.polling(none_stop=True)