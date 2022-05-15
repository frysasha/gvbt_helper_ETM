import telebot
import pathlib
from telebot import types
import time
from socket import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


HOST = '172.29.30.2' #для сообщений на Р2Д2
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST, PORT)
uCliSock = socket(AF_INET, SOCK_DGRAM)

HOST2 = '172.29.2.125' #для сообщений на АСК
PORT2 = 3000
BUFSIZE2 = 1024
SOCKADDR2 = (HOST2, PORT2)

HOST3 = '172.29.50.200' #телевизор
SOCKADDR3 = (HOST3, PORT)

photopath = 'Z:\\python\\ASK\\screenshots\\' #куда сохраняются скрины

TG_TOKEN = "1290310178:AAHtDdkZijsIPb3CDvRcYe78cMb4gbPcavk"
TG_API_URL = 'https://api.telegram.org/bot'
bot = telebot.TeleBot(TG_TOKEN)
proxy = 'http://83.97.23.90:18080'

testchannelid = "-750457583" # gvbt2021F
zabbixcpchannel = '-1001208212827' #заббикс цп
ask_channel_id = "-713732030" # ASK ETM channel
frychannelid = "423057805"
sklad_channel = '-784067672'
gvbt_replykeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
sklad_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)#кнопка снизу клавы
gvbt_replykeyboard.row('LAPS 🔐', 'АСК Пауза 🤖', 'АСК в работу 🤖', 'Расписание ГВБТ 📅') # первая строка меню
gvbt_replykeyboard.row('Статистика поломок общая','Статистика починок общая') # вторая строка меню
gvbt_replykeyboard.row('Статистика за текущий месяц') # третья строка меню
sklad_keyboard.row('АСК Пауза 🤖', 'АСК в работу 🤖', 'Расписание ГВБТ 📅')

inl_keyboard = types.InlineKeyboardMarkup() #кнопка в сообщении
inl_keyboard.row(types.InlineKeyboardButton('Поправил', callback_data='popravil'))
inl_keyboard2 = types.InlineKeyboardMarkup()
inl_keyboard2.row(types.InlineKeyboardButton('Поправил', callback_data='popravil'))
inl_keyboard2.row(types.InlineKeyboardButton('Решение', callback_data='reshenie'))
inl_keyboard3 = InlineKeyboardMarkup([[InlineKeyboardButton('Поправил', callback_data='popravil')]])


filepathpriem = pathlib.Path('V:\\priem.rps\\logs\\faults.log') #пути до логов
filepathblue = pathlib.Path('V:\\blue.rps\logs\\faults.log')
filepathyellow = pathlib.Path('V:\\yellow.rps\\logs\\faults.log')

nowtimedate = time.strftime("%d.%m.%Y %H:%M:%S")

timepriem = filepathpriem.stat().st_mtime #время в секундах
timeblue = filepathblue.stat().st_mtime
timeyellow = filepathyellow.stat().st_mtime
