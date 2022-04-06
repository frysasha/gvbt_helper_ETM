
import pathlib
from funcbot import *
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters
import time
from time import sleep
from settingsbot import *
import threading
import sys
from db import db_regular_insert, db_who_is_most_broken_in_current_month
from socket import *
import datetime

HOST = ''
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
uServSock = socket(AF_INET,SOCK_DGRAM)
uServSock.bind(SOCKADDR)

def proverka ():

    global timepriem, last_modpriem, last_modblue, last_modyellow, timeblue, timeyellow
    while True:
        nowtime = time.strftime("%H:%M:%S")  # текущее время
        strnowtime = str(time.strftime("%d.%m.%Y %H:%M:%S"))
        try:
            last_modpriem = filepathpriem.stat().st_mtime
            last_modblue = filepathblue.stat().st_mtime
            last_modyellow = filepathyellow.stat().st_mtime
        except Exception:
            print('нет доступа к логам!' + strnowtime)
            sleep(5)

        if last_modpriem > timepriem:
            priem_robot.send_error(bot, nowtime)
            #priem_msg(bot, nowtime)
            timepriem = last_modpriem
            print('Ошибка приемного робота в ' + strnowtime)
            db_regular_insert(robot='Приемный', date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modblue > timeblue:
            blue_robot.send_error(bot, nowtime)
            #blue_msg(bot, nowtime)
            timeblue = last_modblue
            print('Ошибка голубого робота в ' + strnowtime)
            db_regular_insert(robot='Голубой', date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modyellow > timeyellow:
            yellow_robot.send_error(bot, nowtime)
            #yellow_msg(bot, nowtime)
            timeyellow = last_modyellow
            print('Ошибка желтого робота в ' + strnowtime)
            db_regular_insert(robot='Желтый', date=time.strftime("%Y-%m-%d"), time=nowtime)

        sleep(1)

def napominanie():

    while True:
        nowdatetime = time.strftime("%a:%H:%M:%S")
        if (time.strftime("Sun:22:35:00")) == nowdatetime:
            napominanie_msg(bot)
        sleep(1)

def robot_stat():
    pass
    # while True:
    #     nowtime = time.strftime("%d %H:%M:%S")
    #     if (time.strftime("01 09:10:00")) == nowtime:
    #         bot_mes('Ещемесячная статистика\n')
    #         every_month_statistic_bot(bot, int(time.strftime("%m")) - 1)
    #     sleep(1)

def wms_report():
    while True:
        data, addr = uServSock.recvfrom(BUFSIZE)
        loc_data = data.decode('cp1251')
        if loc_data == 'Сформирован ежедневный отчет WMS. Необходимо проверить данные!':
            print('Сформирован ежедневный отчет WMS. Необходимо проверить данные!')
            wms_day_report_message(bot)
        elif loc_data == 'Есть решение':
            print('Есть решение ошибки робота')
            yellow_robot.update_inline_button(bot)
        else:
            wms_day_report_error_message(bot, loc_data)

thread1 = threading.Timer(1, proverka)
thread2 = threading.Timer(1, napominanie)
thread3 = threading.Timer(1, robot_stat)
thread4 = threading.Timer(1, wms_report)

try:
    thread1.start()
except Exception:
    robot_oshibka(bot)
    print('ошибка thread1')
try:
    thread2.start()
except Exception:
    robot_oshibka(bot)
    print('ошибка thread2')
try:
    thread3.start()
except Exception:
    print('ошибка thread3')

try:
    thread4.start()
except Exception:
    print("ошибка thread4")



