
import pathlib
from funcbot import *
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters
import time
from time import sleep
from settingsbot import *
import threading
import sys
import logging
from updater import *
from socket import *

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


        if last_modblue > timeblue:

            blue_msg(bot, nowtime)
            timeblue = last_modblue
            bluecount += 1
            logging.info('№' + str(bluecount) + ' Ошибка голубого робота в ' + strnowtime)
            print(str(bluecount) + ' Ошибка голубого робота в ' + strnowtime)


        if last_modyellow > timeyellow:
            yellow_msg(bot, nowtime)
            timeyellow = last_modyellow
            yellowcount += 1
            logging.info('№' + str(yellowcount) + ' Ошибка желтого робота в ' + strnowtime)
            print(str(yellowcount) + ' Ошибка желтого робота в ' + strnowtime)


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

def start_to_update():
    while True:
        nowtime = time.strftime("%H:%M:%S")
        #print(nowtime)
        if (time.strftime("--------------21:30:00")) == nowtime:
            print('время проверки новых программ')
            firefox_update86()
            firefox_update64()
            skype_update()
            cristaldisk_update()
            zip_update()
            cc_update()
            tvnc_update()
            google_update64()
            google_update86()
            zoom_update()
        time.sleep(1)

def wms_report():
    while True:
        data, addr = uServSock.recvfrom(BUFSIZE)
        loc_data = data.decode('cp1251')
        if loc_data == 'Wms Day Report complete':
            print('Wms Day Report complete')
            wms_day_report_message(bot)
        else:
            wms_day_report_error_message(bot, loc_data)


thread1 = threading.Timer(1, proverka)
thread2 = threading.Timer(1, napominanie)
thread3 = threading.Timer(1, start_to_update)
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



