
from time import sleep, strftime
from settingsbot import *
import subprocess
import re
from telegram.ext import ConversationHandler
import os
from PIL import Image
from db import db_update_who_repair, db_who_is_most_broken_off_all_time, db_who_fixed_the_most_off_all_time, \
    db_who_is_most_broken_in_current_month, db_who_fixed_in_current_month
import websocket
import re
from contextlib import closing

def all_statistic_bot(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_is_most_broken_off_all_time()))

def bot_mes(mes):
    bot.send_message(testchannelid, mes)

def all_statistic_gvbt(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_fixed_the_most_off_all_time()))

def month_statistic_bot(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_is_most_broken_in_current_month(time.strftime("%m"))))
    context.bot.send_message(update.message.chat_id, str(db_who_fixed_in_current_month(time.strftime("%m"))))

def every_month_statistic_bot(bot, month):
    bot.send_message(testchannelid, str(db_who_is_most_broken_in_current_month(month)))
    bot.send_message(testchannelid, str(db_who_fixed_in_current_month(month)))


def welcome_message (bot):
    bot.send_message(frychannelid, 'Старт бота', reply_markup=inl_keyboard2)
    #bot.send_message(testchannelid, 'Старт бота', reply_markup=gvbt_replykeyboard)
    #bot.send_message(ask_channel_id, 'Старт бота', reply_markup=gvbt_replykeyboard)
    #bot.send_message(sklad_channel, 'Старт бота', reply_markup=sklad_keyboard) #вывод нижней клавы


class Robot:

    last_mes_id = ''

    def __init__(self, sticker, name, eng_name, log_file, ws_port):
        self.sticker = sticker
        self.name = name
        self.eng_name = eng_name
        self.resolve_flag = True
        resolve_flag = True
        self.log_file = log_file
        self.ws_port = ws_port

    def send_error(self, bot, time):
        last_broken_robot = self.eng_name
        bot.send_sticker(ask_channel_id, self.sticker)
        send = bot.send_message(ask_channel_id, str(self.name + ' робот ошибка в ' + str(time)), reply_markup=inl_keyboard)
        global last_mes_id
        last_mes_id = send.message_id
        uCliSock.sendto(bytes(self.name + ' робот ошибка', 'cp1251'), SOCKADDR)  # отправка текста на сервер спикера
        uCliSock.sendto(bytes(self.eng_name, 'utf-8'), SOCKADDR2)  # отправка на сервер АСК
        sleep(1)
        yellow_robot.resolve_flag = True
        bot.send_message(ask_channel_id, self.send_error_text())
        #bot.send_photo(ask_channel_id, photo=open(photopath + self.eng_name + '.png', 'rb'))  # отправка скрина
        sleep(5)
        bot.send_message(ask_channel_id, self.check_ws_state())

    def check_ws_state(self):
        with closing(websocket.create_connection('ws://172.29.2.125:' + self.ws_port + '/wscChannel')) as wd:
            res = (re.search('"CMD_STATE": "(\w+)', wd.recv()).group(1))
        return res

    def send_error_text(self):
        with open(self.log_file, 'r') as f:
            last_line = f.readlines()[-2]
            return last_line


def update_inline_button(bot):
    try:
        bot.edit_message_reply_markup(ask_channel_id, message_id=last_mes_id, reply_markup=inl_keyboard2)
        yellow_robot.resolve_flag = False
    except:
        print('Не удалось найти последнее сообщение')
        yellow_robot.resolve_flag = False


priem_robot = Robot(sticker='CAACAgIAAxkBAAEBV-5fY1yzqRqG6hFdFnC0OmD98UKzSQACBAADjVk3GTq8TbLpDM2NGwQ',
                    name='Приемный', eng_name='priem', log_file='V:\\priem.rps\\logs\\faults.log', ws_port=8003)
blue_robot = Robot(sticker='CAACAgIAAxkBAAEBV6BfYwNb-miwdeZwoM0mY88-6tBJQAACAwADjVk3GYsJmaauajlLGwQ',
                   name='Синий', eng_name='blue', log_file='V:\\blue.rps\logs\\faults.log', ws_port=8001)
yellow_robot = Robot(sticker='CAACAgIAAxkBAAEBV5xfYwMsdhZK_ojtyb9q1l48Et6EZwACAQADjVk3GTWKtUGHR0TKGwQ',
                     name='Желтый', eng_name='yellow', log_file='V:\\yellow.rps\\logs\\faults.log', ws_port=8002)


def inline_popravil_button_pressed(bot, update):
    query = bot.callback_query
    update.bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id, reply_markup='')  # убирает кнопку в сообщении
    update.bot.send_message(ask_channel_id, f'Робота поправил {query.from_user.first_name} спасибо!')

    print(f'Робота поправил {query.from_user.first_name} в {time.strftime("%d.%m.%Y %H:%M:%S")}')
    db_update_who_repair(query.from_user.first_name)

def inline_reshenie_button_pressed(bot, update):
    query = bot.callback_query
    yellow_robot.resolve_flag = False
    update.bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id, reply_markup=inl_keyboard3) #оставляетс только кнопку "Поправил"
    update.bot.send_message(ask_channel_id, f'Пробую решить ошибку')
    uCliSock.sendto(bytes('Resolve problem', 'utf-8'), SOCKADDR2)
    print(f'{query.from_user.first_name} в {time.strftime("%d.%m.%Y %H:%M:%S")} нажал кнопку "Решение"')


def napominanie_msg(bot):
    uCliSock.sendto(bytes('perezagruzka', 'cp1251'), SOCKADDR2)
    uCliSock.sendto(bytes('restart_televizor', 'cp1251'), SOCKADDR3)
    sleep(5)
    bot.send_message(ask_channel_id, ('Будет запущен АСК и включен телик на складе после еженедельной перезагрузки!'))
    bot.send_photo(ask_channel_id, photo=open(photopath + 'perezagruzka.png', 'rb'))  # отправка скрина

def wms_day_report_message(bot):
    today = time.strftime("%d.%m.%Y")
    report_file = 'C:\\Users\\shlyakhov_ai\\PycharmProjects\\WMS_Report 2\\отчеты\\' + today + '.xlsx'
    bot.send_message(testchannelid, ('Сформирован ежедневный отчет WMS. Необходимо проверить данные!'))
    wmsreport = open(report_file, 'rb')
    bot.send_document(testchannelid, wmsreport)
    wmsreport.close()

def wms_day_report_error_message(bot, message):
    bot.send_message(testchannelid, message)

def laps_start(bot, update):
    bot.message.reply_text('Веедите имя компьютера')
    return "user_name" #возвращает тому, кто прислал сообщение

def writetofile(message):
    doc = open('C:\\python\\name.txt', 'w')
    doc.write(message)
    doc.close()
    sleep(1)
    startbat()

def startbat():
    p = subprocess.Popen('C:\\python\\start.start.bat')

def laps_zapros(bot, update):
    update.user_data['name'] = bot.message.text
    textmes = (bot.message.text)
    rex = re.compile("^[0-9]{4}-[0-9]{3}[A-z]{2}$") #формат текста [тип текста] , {кол-во символов} , ^ начало , $ конец
    if rex.match(textmes):
        writetofile(bot.message.text)
        sleep(4)
        cleantext2 = []
        if os.stat('C:\\python\\pass.txt').st_size == 0:
            net_parolya()
        else:
            for i in open('C:\\python\\pass.txt', 'r', encoding='utf-16').readlines():
                cleantext2.append(i)
            cleantext2 = cleantext2[-3][-13:].strip()
            print(f'Запрашиваемый пароль: {cleantext2}')
            laps_send_msg(f'пароль: {cleantext2}')
        return ConversationHandler.END  # закрывает диалог


    else:
        laps_format_msg()

def laps_format_msg():
    bot.send_message(testchannelid, 'неправильный формат! нужен формат вида "0200-300PC')

def net_parolya():
    bot.send_message(testchannelid, 'пароль не найден')

def laps_send_msg(cleantext):
    bot.send_message(testchannelid, cleantext) #сообщение с паролем

def robot_oshibka(bot):
    bot.send_message(ask_channel_id, "Боту плохо, нужно его перезарустить!")
    print("Боту плохо, нужно его перезарустить!")

def ask_pause_button(update, context):
    uCliSock.sendto(bytes('pause_button', 'cp1251'), SOCKADDR2)
    print('pause_button')
    sleep(5)
    im = Image.open(r'Z:\python\ASK screenshots\pause.png')
    im.crop((810, 670, 1020, 780)).save(photopath + 'pause_new.png', quality=95)
    sleep(1)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(photopath + 'pause_new.png', 'rb'))

def ask_work_button(update, context):
    uCliSock.sendto(bytes('work_button', 'cp1251'), SOCKADDR2)
    print('work_button')
    sleep(5)
    im = Image.open(r'Z:\python\ASK screenshots\work.png')
    im.crop((810, 670, 1020, 780)).save(photopath + 'work_new.png', quality=95)
    sleep(1)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(photopath + 'work_new.png', 'rb'))

def schedule(update, context):
    path = 'Z:\\python\\расписание\\'
    try:
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(path + time.strftime('%m') + '.jpg', 'rb'))
    except:
        context.bot.send_message(update.message.chat_id, 'Нет расписания на текущий месяц')


if __name__ == "__main__":
    pass
    #print(db_who_fixed_in_current_month(strftime('%m')))
    # print(str(db_who_fixed_the_most_off_all_time()))
    #print(str(db_who_is_most_broken_in_current_month()))
    #print(str(db_who_is_most_broken_in_current_month(strftime('%m'))))
    # month_statistic_gvbt(bot)
    # month_statistic_bot(bot)
    #print(every_month_statistic_bot(bot, int(time.strftime("%m")) - 1))
