
from time import sleep
from settingsbot import *
import subprocess
import re
from telegram.ext import ConversationHandler
import os


#from mainbot import bot

def update_message (bot, prog, ver):
    bot.send_sticker(testchannelid, 'CAACAgIAAxkBAAECNtBggUpZtX57WXfnT-saEaXxUOBM0QACygADq1fEC3fQ4RKXbxJiHwQ')
    bot.send_message(testchannelid, 'Успешно скачалась новая версия ' + prog + ' ' + ver)


def welcome_message (bot):
    pass
    ##bot.send_message(ask_channel_id, 'start bot', reply_markup=replykeyboard) #вывод нижней клавы

def inline_button_pressed(bot, update):
    query = bot.callback_query
    update.bot.send_message(ask_channel_id, 'Робота поправили! спасибо')
    update.bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id, reply_markup='') #убирает кнопку в сообщении

def priem_msg(bot, time):
    bot.send_sticker(ask_channel_id, 'CAACAgIAAxkBAAEBV-5fY1yzqRqG6hFdFnC0OmD98UKzSQACBAADjVk3GTq8TbLpDM2NGwQ')
    bot.send_message(ask_channel_id, ('Приемный робот ошибка в ' + str(time)), reply_markup=inl_keyboard)  # пишет ошибку, время и добавляет кнопку
    uCliSock.sendto(bytes('Приемный робот ошибка', 'cp1251'), SOCKADDR) #отправка текста на сервер спикера
    uCliSock.sendto(bytes('priem', 'cp1251'), SOCKADDR2)  # отправка на сервер АСК
    sleep(4)
    bot.send_photo(ask_channel_id, photo=open(photopath + 'priem.png', 'rb')) #отправка скрина

    #data, addr = uCliSock.recvfrom(BUFSIZE)

def blue_msg(bot, time):

    bot.send_sticker(ask_channel_id, 'CAACAgIAAxkBAAEBV6BfYwNb-miwdeZwoM0mY88-6tBJQAACAwADjVk3GYsJmaauajlLGwQ')
    bot.send_message(ask_channel_id, ('Голубой робот ошибка в ' + str(time)), reply_markup=inl_keyboard)  # пишет ошибку, время и добавляет кнопку
    uCliSock.sendto(bytes('Синий робот ошибка', 'cp1251'), SOCKADDR) #отправка текста на сервер спикера
    uCliSock.sendto(bytes('blue', 'cp1251'), SOCKADDR2)  # отправка на сервер АСК
    sleep(4)
    bot.send_photo(ask_channel_id, photo=open(photopath + 'blue.png', 'rb')) #отправка скрина
    #data, addr = uCliSock.recvfrom(BUFSIZE)

def yellow_msg(bot, time):

    bot.send_sticker(ask_channel_id, 'CAACAgIAAxkBAAEBV5xfYwMsdhZK_ojtyb9q1l48Et6EZwACAQADjVk3GTWKtUGHR0TKGwQ')
    bot.send_message(ask_channel_id, ('Желтый робот ошибка в ' + str(time)), reply_markup=inl_keyboard)  # пишет ошибку, время и добавляет кнопку
    uCliSock.sendto(bytes('Желтый робот ошибка', 'cp1251'), SOCKADDR) #отправка текста на сервер спикера
    uCliSock.sendto(bytes('yellow', 'cp1251'), SOCKADDR2) #отправка на сервер АСК
    sleep(5)
    bot.send_photo(ask_channel_id, photo=open(photopath + 'yellow.png', 'rb')) #отправка скрина
    #data, addr = uCliSock.recvfrom(BUFSIZE)

def napominanie_msg(bot):
    uCliSock.sendto(bytes('perezagruzka', 'cp1251'), SOCKADDR2)
    uCliSock.sendto(bytes('restart_televizor', 'cp1251'), SOCKADDR3)
    sleep(5)
    bot.send_message(ask_channel_id, ('Будет запущен АСК и включен телик на складе после еженедельной перезагрузки!'))
    bot.send_photo(ask_channel_id, photo=open(photopath + 'perezagruzka.png', 'rb'))  # отправка скрина

def wms_day_report_message(bot):
    today = time.strftime("%d.%m.%Y")
    reportpath = ('C:\\python\\WMS_Day_Report\\finaldayreport ' + today + '.txt')
    bot.send_message(testchannelid, ('Сформирован ежедневный отчет WMS. Необходимо проверить данные!'))
    wmsreport = open(reportpath, 'r', encoding='cp1251')
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
        for i in open('C:\\python\\pass.txt', 'r', encoding='utf-16').readlines():
            cleantext2.append(i)
        cleantext2 = cleantext2[-3][-13:].strip()
        print(f'Запрашиваемый пароль: {cleantext2}')
        #read_text = open('C:\\python\\pass.txt', 'r')#, encoding='utf-16')
        if os.stat('C:\\python\\pass.txt').st_size == 0:
            net_parolya()
        laps_send_msg(f'пароль: {cleantext2}')
        return ConversationHandler.END  # закрывает диалог
        # else:
        #     rtext = read_text.read()
        #     #print(rtext)
        #if len(rtext) > 460: #убирает первые 460 символов
            #cleantext = ('пароль: ' + rtext[460:].lstrip())
            #print(type(cleantext))
            #print(cleantext)

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

def ask_pause_button(bot, context):
    uCliSock.sendto(bytes('pause_button', 'cp1251'), SOCKADDR2)
    print('pause_button')
    sleep(5)
    context.bot.send_photo(ask_channel_id, photo=open(photopath + 'pause.png', 'rb'))  # отправка скрина
    #return ConversationHandler.END

def ask_work_button(bot, context):
    uCliSock.sendto(bytes('work_button', 'cp1251'), SOCKADDR2)
    print('work_button')
    sleep(5)
    context.bot.send_photo(ask_channel_id, photo=open(photopath + 'work.png', 'rb'))  # отправка скрина
    #return ConversationHandler.END



