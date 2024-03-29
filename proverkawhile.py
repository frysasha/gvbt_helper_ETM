from socket import socket, AF_INET, SOCK_DGRAM
import time
from time import sleep
import threading
from funcbot import priem_robot, blue_robot, yellow_robot, napominanie_msg, every_month_statistic_bot, \
    wms_day_report_message, Robot, update_inline_button, bot_mes
from settingsbot import filepathpriem, filepathblue, filepathyellow, bot, timeblue, timepriem, timeyellow

HOST = ''
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST, PORT)



def proverka():
    global last_modpriem, last_modblue, last_modyellow, timepriem, timeblue, timeyellow
    while True:
        nowtime = time.strftime("%H:%M:%S")  # текущее время
        strnowtime = str(time.strftime("%d.%m.%Y %H:%M:%S"))
        try:
            last_modpriem = filepathpriem.stat().st_mtime
            last_modblue = filepathblue.stat().st_mtime
            last_modyellow = filepathyellow.stat().st_mtime
        except Exception:
            print('нет доступа к логам!' + strnowtime)
            sleep(30)

        if last_modpriem > timepriem:
            priem_robot.send_error(bot, nowtime)
            timepriem = last_modpriem
            print('Ошибка приемного робота в ' + strnowtime)
            priem_robot.db_error_insert(date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modblue > timeblue:
            blue_robot.send_error(bot, nowtime)
            timeblue = last_modblue
            print('Ошибка голубого робота в ' + strnowtime)
            blue_robot.db_error_insert(date=time.strftime("%Y-%m-%d"), time=nowtime)

        if last_modyellow > timeyellow:
            yellow_robot.send_error(bot, nowtime)
            timeyellow = last_modyellow
            print('Ошибка желтого робота в ' + strnowtime)
            yellow_robot.db_error_insert(date=time.strftime("%Y-%m-%d"), time=nowtime)

        sleep(1)


def napominanie():
    while True:
        nowdatetime = time.strftime("%a:%H:%M:%S")
        if (time.strftime("Sun:22:35:00")) == nowdatetime:
            napominanie_msg(bot)
        sleep(1)


def ask_month_stat():
    while True:
        nowtime = time.strftime("%d %H:%M:%S")
        if (time.strftime("01 10:00:00")) == nowtime:
            prev_month = str('0' + str(int(time.strftime("%m")) - 1)) if int(time.strftime("%m")) < 10 else int(
                time.strftime("%m")) - 1
            if prev_month == '00':
                prev_month = '12'
            try:
                every_month_statistic_bot(bot, prev_month)
            except:
                print(' every_month_statistic_bot error')
        sleep(1)


def udp_client():
    uServSock = socket(AF_INET, SOCK_DGRAM)
    uServSock.bind(SOCKADDR)
    while True:
        try:
            data, addr = uServSock.recvfrom(BUFSIZE)
            loc_data = data.decode('cp1251')
            if loc_data == 'Сформирован ежедневный отчет WMS. Необходимо проверить данные!':
                print('Сформирован ежедневный отчет WMS. Необходимо проверить данные!')
                wms_day_report_message(bot)
            elif loc_data == 'Est reshenie':
                if Robot.resolve_flag:
                    update_inline_button(bot)
            elif 'LOOP_PROT' in str(loc_data):
                bot_mes('Петля в коммутаторе!\n\n' + loc_data)
        except Exception as e:
            print(f'err thread 4: {e}')


thread1 = threading.Timer(1, proverka)
thread2 = threading.Timer(1, napominanie)
thread3 = threading.Timer(1, ask_month_stat)
thread4 = threading.Timer(1, udp_client)
def main_threads():
    try:
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

    except Exception:
        print(Exception)


if __name__ == '__main__':
    main_threads()
