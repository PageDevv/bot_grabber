from threading import Thread
from pyrogram import Client, filters
import telebot

userbot = Client("userbot", api_id, "api_hash")  # данные бота

my_bot = telebot.TeleBot("token")  # token бота

pars_bot = 123456  # id бота у которого будем парсить

users = []

start_text = """Вы подписались на рассылку"""  # текст, который пишется при написании /start нашему боту


@userbot.on_message(filters=~filters.me)
def on_message(client, message):
    if message.chat.id == pars_bot:
        post_message(message.text)


@my_bot.message_handler(commands=["start"])
def start(message):
    get_data()
    if message.chat.id not in users:
        users.append(message.chat.id)
        write_data()
	my_bot.send_message(message.chat.id, start_text)


def post_message(message):
    get_data()
    for user in users:
        my_bot.send_message(user, message)


def get_data():
    global users
    with open("data.txt", "r") as file:
        users = eval(file.read())
        file.close()


def write_data():
    with open("data.txt", "w") as file:
        file.write(str(users))
        file.close()


print("Starting")
t1 = Thread(target=my_bot.polling)
print("Thread started")
t1.start()

userbot.run()

t1.join()
