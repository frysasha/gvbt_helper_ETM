from socket import socket, AF_INET, SOCK_DGRAM
from telebot import types, TeleBot
import pathlib
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

HOST = '172.29.30.62' #для сообщений на Р2Д2
PORT = 3001
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
bot = TeleBot(TG_TOKEN)
proxy = 'http://83.97.23.90:18080'

testchannelid = "-1001508813774"  #"-750457583" # gvbt2021F
zabbixcpchannel = '-1001208212827' #заббикс цп
ask_channel_id = "-1001598599638"  #"-713732030" # ASK ETM channel

frychannelid = "423057805"
sklad_channel = "-1001634933123"  #'-784067672'
gvbt_replykeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
sklad_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
gvbt_replykeyboard.row('LAPS 🔐', 'АСК Пауза 🤖', 'АСК в работу 🤖', 'Расписание ГВБТ 📅')
gvbt_replykeyboard.row('Статистика поломок общая', 'Статистика починок общая')
gvbt_replykeyboard.row('Статистика за текущий месяц', '/Admin', '/WMS')
sklad_keyboard.row('АСК Пауза 🤖', 'АСК в работу 🤖')
sklad_keyboard.row('Расписание ГВБТ 📅', '/WMS')

inl_keyboard = types.InlineKeyboardMarkup() #кнопка в сообщении
inl_keyboard.row(InlineKeyboardButton('Поправил', callback_data='popravil'))
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

ADMIN_URERS_ID = [423057805, 237426192]


