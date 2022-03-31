
import pathlib
from funcbot import *
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters
import time
from time import sleep
from settingsbot import *
import threading
import sys
from db import db_regular_insert, db_who_is_most_broken_in_current_month
from updater import *
from socket import *
import datetime


logging.basicConfig(filename='robots.log', level=logging.INFO, format='%(message)s')

priemcount = 0
bluecount = 0
yellowcount = 0
testcount = 0
HOST = ''
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
uServSock = socket(AF_INET,SOCK_DGRAM)
uServSock.bind(SOCKADDR)

def start(loginfo):
    logging.info(loginfo)
    print(loginfo)

def proverka ():

    global timepriem, last_modpriem, last_modblue, last_modyellow
    global timeblue
    global timeyellow
    global priemcount
    global bluecount
    global yellowcount

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

            priem_msg(bot, nowtime)
            timepriem = last_modpriem
            priemcount += 1
            logging.info('№' + str(priemcount) + ' Ошибка примного робота в ' + strnowtime)
            print(str(priemcount) + ' Ошибка примного робота в ' + strnowtime)
            db_regular_insert(robot='Приемный', date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modblue > timeblue:

            blue_msg(bot, nowtime)
            timeblue = last_modblue
            bluecount += 1
            logging.info('№' + str(bluecount) + ' Ошибка голубого робота в ' + strnowtime)
            print(str(bluecount) + ' Ошибка голубого робота в ' + strnowtime)
            db_regular_insert(robot='Голубой', date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modyellow > timeyellow:
            yellow_msg(bot, nowtime)
            timeyellow = last_modyellow
            yellowcount += 1
            logging.info('№' + str(yellowcount) + ' Ошибка желтого робота в ' + strnowtime)
            print(str(yellowcount) + ' Ошибка желтого робота в ' + strnowtime)
            db_regular_insert(robot='Желтый', date=time.strftime("%Y-%m-%d"), time=nowtime)

        sleep(3)

def napominanie():
    global testcount

    while True:
        nowtime = time.strftime("%H:%M:%S")
        nowdatetime = time.strftime("%a:%H:%M:%S")
        strnowtime = str(nowtime)

        if (time.strftime("Sun:22:35:00")) == nowdatetime:
            napominanie_msg(bot)
        sleep(1)

def robot_stat():
    while True:
        nowtime = time.strftime("%d %H:%M:%S")
        if (time.strftime("01 09:00:00")) == nowtime:
            month_statistic_bot(bot, int(time.strftime("%m")) - 1)
            month_statistic_gvbt(bot, int(time.strftime("%m")) - 1)
        sleep(1)

def wms_report():
    while True:
        try:
            data, addr = uServSock.recvfrom(BUFSIZE)
            loc_data = data.decode('cp1251')
            if loc_data == 'Сформирован ежедневный отчет WMS. Необходимо проверить данные!':
                print('Сформирован ежедневный отчет WMS. Необходимо проверить данные!')
                wms_day_report_message(bot)
            else:
                wms_day_report_error_message(bot, loc_data)
        except Exception as e:
            print('ошибка отправки результата wms report')
            print(e)


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



