import csv
import subprocess
from datetime import datetime
from time import sleep, strftime
from telegram.ext import ConversationHandler
from telegram.error import BadRequest
import os
from PIL import Image
from data_base.db_requests import db_update_who_repair, db_who_is_most_broken_off_all_time, \
    db_who_fixed_the_most_off_all_time, \
    db_who_is_most_broken_in_current_month, db_who_fixed_in_current_month, db_who_win_in_prev_month, \
    db_update_auto_repair, db_error_insert, db_ask_cell_stat
import websocket
import re
from contextlib import closing
from settings import bot, GVBT_CHANNEL, ASK_CHANNEL_ID, FRYCHANNELID, SKLAD_CHANNEL, gvbt_reply_keyboard, \
    sklad_keyboard, inl_keyboard, uCliSock, SOCKADDR2, SOCKADDR, inl_keyboard2, inl_keyboard3, SOCKADDR3, photopath


def all_statistic_bot(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_is_most_broken_off_all_time()))


def bot_mes(mes):
    bot.send_message(GVBT_CHANNEL, mes)


def all_statistic_gvbt(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_fixed_the_most_off_all_time()))


def month_statistic_bot(update, context):
    context.bot.send_message(update.message.chat_id, str(db_who_is_most_broken_in_current_month(strftime("%Y-%m"))))
    context.bot.send_message(update.message.chat_id,
                             f'Кто чинил:\n{str(db_who_fixed_in_current_month(strftime("%Y-%m")))}')


def every_month_statistic_bot(bot, year_month):
    bot.send_message(ASK_CHANNEL_ID, str(db_who_is_most_broken_in_current_month(year_month)))
    bot.send_message(ASK_CHANNEL_ID, f'Кто чинил:\n{str(db_who_fixed_in_current_month(year_month))}')
    bot.send_message(ASK_CHANNEL_ID, f'И выигрывает приз!!!\n{db_who_win_in_prev_month(year_month)}')


def welcome_message(bot):
    bot.send_message(FRYCHANNELID, 'Старт бота', reply_markup=gvbt_reply_keyboard)
    bot.send_message(GVBT_CHANNEL, 'Старт бота', reply_markup=gvbt_reply_keyboard)
    bot.send_message(ASK_CHANNEL_ID, 'Старт бота', reply_markup=gvbt_reply_keyboard)
    bot.send_message(SKLAD_CHANNEL, 'Старт бота', reply_markup=sklad_keyboard)  # вывод нижней клавы


def error_hand(update, context):
    print('Ошибка error handler')
    if isinstance(context.error, BadRequest):
        pass
    else:
        print(context.error)


class Robot:
    last_mes_id = None
    last_broken_robot = None
    resolve_flag = True

    def __init__(self, sticker, name, eng_name, log_file, ws_port):
        self.sticker = sticker
        self.name = name
        self.eng_name = eng_name
        self.log_file = log_file
        self.ws_port = ws_port

    def send_error(self, bot, time):
        global last_broken_robot
        global last_mes_id
        last_broken_robot = self
        bot.send_sticker(ASK_CHANNEL_ID, self.sticker)
        send = bot.send_message(ASK_CHANNEL_ID, str(self.name + ' робот ошибка в ' + str(time)),
                                reply_markup=inl_keyboard)
        last_mes_id = send.message_id
        uCliSock.sendto(bytes(self.name + ' робот ошибка', 'cp1251'), SOCKADDR)  # отправка текста на сервер спикера
        uCliSock.sendto(bytes(self.eng_name + ' robot_error', 'utf-8'), SOCKADDR2)  # отправка на сервер АСК
        Robot.resolve_flag = True
        bot.send_message(ASK_CHANNEL_ID, self.send_error_text())

    def check_ws_state(self):
        with closing(websocket.create_connection('ws://172.29.2.125:' + self.ws_port + '/wscChannel')) as wd:
            res = (re.search('"CMD_STATE": "(\w+)', wd.recv()).group(1))
        return res

    def _check_ws_cmd(self):
        with closing(websocket.create_connection('ws://172.29.2.125:' + self.ws_port + '/wscChannel')) as wd:
            res = (re.search('"CMD": "(\w+\s\w+)', wd.recv()).group(1))
        return res

    def _check_ws_section(self):
        with closing(websocket.create_connection('ws://172.29.2.125:' + self.ws_port + '/wscChannel')) as wd:
            res = (re.search('"SECTION": "(\w+)', wd.recv()).group(1))
        return res

    def send_error_text(self):
        with open(self.log_file, 'r') as f:
            last_line = f.readlines()[-2]
            return last_line

    def search_fault_text(self):
        try:
            with open(self.log_file, 'r') as f:
                last_line = f.readlines()[-2]
                res = (re.search('faults:\((.+)\)', last_line).group(1))
                return res
        except:
            return 'no fault'

    def db_error_insert(self, date, time):
        db_error_insert(robot=self.name, date=date, time=time, cmd=self._check_ws_cmd(),
                        section=self._check_ws_section(),
                        faults=self.search_fault_text())


def update_inline_button(bot):
    try:
        bot.edit_message_reply_markup(ASK_CHANNEL_ID, message_id=last_mes_id, reply_markup=inl_keyboard2)
        Robot.resolve_flag = False
    except:
        print('Не удалось найти последнее сообщение')
        Robot.resolve_flag = False


priem_robot = Robot(sticker='CAACAgIAAxkBAAEBV-5fY1yzqRqG6hFdFnC0OmD98UKzSQACBAADjVk3GTq8TbLpDM2NGwQ',
                    name='Приемный', eng_name='priem', log_file=r'V:\priem.rps\logs\faults.log', ws_port="8003")
blue_robot = Robot(sticker='CAACAgIAAxkBAAEBV6BfYwNb-miwdeZwoM0mY88-6tBJQAACAwADjVk3GYsJmaauajlLGwQ',
                   name='Голубой', eng_name='blue', log_file=r'V:\blue.rps\logs\faults.log', ws_port="8001")
yellow_robot = Robot(sticker='CAACAgIAAxkBAAEBV5xfYwMsdhZK_ojtyb9q1l48Et6EZwACAQADjVk3GTWKtUGHR0TKGwQ',
                     name='Желтый', eng_name='yellow', log_file=r'V:\yellow.rps\logs\faults.log', ws_port="8002")


def inline_popravil_button_pressed(bot, update):
    query = bot.callback_query
    update.bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id, reply_markup='')  # убирает кнопку в сообщении
    update.bot.send_message(ASK_CHANNEL_ID, f'Робота поправил {query.from_user.first_name} спасибо!')
    print(f'Робота поправил {query.from_user.first_name} в {strftime("%d.%m.%Y %H:%M:%S")}')
    uCliSock.sendto(bytes(f'{query.from_user.first_name} поправил робота', 'cp1251'), SOCKADDR)
    db_update_who_repair(query.from_user.first_name)


def inline_reshenie_button_pressed(bot, update):
    query = bot.callback_query
    Robot.resolve_flag = False
    update.bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id, reply_markup=inl_keyboard3)  # оставляетс только кнопку "Поправил"

    try:
        cmd_state_now = last_broken_robot.check_ws_state()
        if cmd_state_now == 'FAILURE':
            update.bot.send_message(ASK_CHANNEL_ID, f'{query.from_user.first_name} нажал кнопку Решение')
            uCliSock.sendto(bytes('Resolve problem', 'utf-8'), SOCKADDR2)
            print(f'{query.from_user.first_name} в {strftime("%d.%m.%Y %H:%M:%S")} нажал кнопку "Решение"')
            uCliSock.sendto(bytes(f'{query.from_user.first_name} нажал кнопку Решение', 'cp1251'), SOCKADDR)
            db_update_auto_repair()
        else:
            update.bot.send_message(ASK_CHANNEL_ID, 'Нет ошибки у робота в данный момент')
    except:
        print('last_broken_robot не определен')
        update.bot.send_message(ASK_CHANNEL_ID, 'last_broken_robot не определен')


def napominanie_msg(bot):
    uCliSock.sendto(bytes('work_button', 'cp1251'), SOCKADDR2)
    uCliSock.sendto(bytes('restart_televizor', 'cp1251'), SOCKADDR3)
    bot.send_message(ASK_CHANNEL_ID,
                     ('Будет запущен АСК и включен телик на складе после еженедельной перезагрузки! Адрес 20.200!!!!'))


def wms_day_report_message(bot):
    today = strftime("%d.%m.%Y")
    report_file = 'S:\\09.ГВБТ\\WMS_Report\\' + today + '.xlsx'
    bot.send_message(GVBT_CHANNEL, ('Сформирован ежедневный отчет WMS. Необходимо проверить данные!'))
    wmsreport = open(report_file, 'rb')
    bot.send_document(GVBT_CHANNEL, wmsreport)
    wmsreport.close()


def laps_start(bot, update):
    bot.message.reply_text('Веедите имя компьютера')
    return "user_name"  # возвращает тому, кто прислал сообщение


def writetofile(message):
    doc = open('C:\\python\\name.txt', 'w')
    doc.write(message)
    doc.close()
    startbat()


def startbat():
    p = subprocess.Popen('C:\\python\\start.start.bat')


def laps_zapros(update, context):
    rex = re.compile(
        "^[0-9]{4}-[0-9]{3}[A-z]{2}$")  # формат текста [тип текста] , {кол-во символов} , ^ начало , $ конец
    if rex.match(update.message.text):
        writetofile(update.message.text)
        sleep(4)
        cleantext2 = []
        if os.stat('C:\\python\\pass.txt').st_size == 0:
            context.bot.send_message(update.message.chat_id, 'пароль не найден')
        else:
            for i in open('C:\\python\\pass.txt', 'r', encoding='utf-16').readlines():
                cleantext2.append(i)
            cleantext2 = cleantext2[2][10:].strip()
            print(f'Запрашиваемый пароль: {cleantext2}')
            laps_send_msg(cleantext2, update, context)
        return ConversationHandler.END  # закрывает диалог
    elif update.message.text == 'exit':
        return ConversationHandler.END
    else:
        context.bot.send_message(update.message.chat_id, 'неправильный формат! нужен формат вида "0200-300PC')


def laps_send_msg(cleantext, update, context):
    context.bot.send_message(update.message.chat_id, cleantext)  # сообщение с паролем


def ask_pause_button(update, context):
    uCliSock.sendto(bytes('pause_button', 'cp1251'), SOCKADDR2)
    print('pause_button')
    sleep(5)
    im = Image.open(r'Z:\python\ASK\screenshots\pause.png')
    im.crop((810, 670, 1020, 780)).save(photopath + 'pause_new.png', quality=95)
    sleep(1)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photopath + 'pause_new.png', 'rb'))


def ask_work_button(update, context):
    uCliSock.sendto(bytes('work_button', 'cp1251'), SOCKADDR2)
    print('work_button')
    sleep(5)
    im = Image.open(r'Z:\python\ASK\screenshots\work.png')
    im.crop((810, 670, 1020, 780)).save(photopath + 'work_new.png', quality=95)
    sleep(1)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photopath + 'work_new.png', 'rb'))


def schedule(update, context):
    path = 'S:\\09.ГВБТ\\Расписание\\'
    try:
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(path + strftime('%m') + '.jpg', 'rb'))

    except:
        context.bot.send_message(update.message.chat_id, 'Нет расписания на текущий месяц')


def cartridge(update, context):
    context.bot.send_message(update.message.chat_id, 'L1 Диспетчерская - Картридж 237\
    \nL2 Комплектация - Картидж 237\nL3 Приемка - Картридж 280\nL4 КПП середина - Картридж 280\
    \nL5 АСК - Картридж 280\nL6 Зона У - Картридж 280\nL7 Зона К - Картридж 3160\
    \nL9 Учеб.класс - Картридж 226\nL10 Доставка - Картридж 226\nL12 КПП начало - Картридж 226\
    \nL13 ГОК - Картридж 237\nL16 ГОК2 - Картридж 259\nL18 Железо - Картридж 226 \
    \nL19 СВК - Картридж 1200 \nL21 КПП конец - Картридж 226\nL22 Зона С - Картридж 2371111 ')


def create_csv_report(db_sql_request, order_by):
    unic_file_name = 'csv_reports\\' + str(datetime.now().strftime('%y%m%d.%H%M%S') + '.csv')
    with open(unic_file_name, 'w') as fp:
        file_to_write = csv.writer(fp, delimiter=';', lineterminator="\r")
        file_to_write.writerow(['Секция', 'Команда', 'Робот', 'Ошибка', 'Дата', 'Время'])
        file_to_write.writerows(db_sql_request(order_by))
    return unic_file_name


if __name__ == "__main__":
    create_csv_report(db_ask_cell_stat, 'date')
    # print(db_who_fixed_in_current_month(strftime('%m')))
    # print(str(db_who_fixed_the_most_off_all_time()))
    # print(str(db_who_is_most_broken_in_current_month()))
    # print(str(db_who_is_most_broken_in_current_month(strftime('%m'))))
    # month_statistic_gvbt(bot)
    # month_statistic_bot(bot)
    # print(every_month_statistic_bot(bot, int(time.strftime("%m")) - 1))
