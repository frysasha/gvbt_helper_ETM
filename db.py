import sqlite3
from datetime import date, timedelta, datetime
import time
from collections import Counter
import calendar

db = sqlite3.connect('robots.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS robot_error(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
   robot TEXT,
   date DATE,
   time TIME,
   who_repair TEXT);
""")
db.commit()


def db_regular_insert(robot, date, time, who_repair=''):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("INSERT INTO robot_error (robot, date, time, who_repair) VALUES (?, ?, ?, ?);", (robot, date, time, who_repair))
    db.commit()
    cur.close()


def db_update_who_repair(who_repair):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("UPDATE robot_error SET who_repair =:who WHERE ID = (SELECT MAX(ID) FROM robot_error)",
                {'who': who_repair})
    db.commit()
    cur.close()

def db_who_is_most_broken_in_current_month(month):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    first_day = datetime.today().replace(day=1).strftime('%Y-' + '0' + str(month) + '-%d')
    plus_month = datetime.today().replace(day=1, month=(int(month)+1))
    last_day = plus_month - timedelta(days=1)
    cur.execute("SELECT robot FROM robot_error WHERE date BETWEEN :date1 AND :date2", {'date1': first_day, 'date2': last_day.strftime('%Y-%m-%d')})
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.execute("SELECT robot FROM robot_error WHERE (time BETWEEN '00:00:00' AND '07:00:00') AND (date BETWEEN :date1 AND :date2)", {'date1': first_day, 'date2': last_day.strftime('%Y-%m-%d')})
    night = cur.fetchall()
    night_list = []
    for i in night:
        night_list.append(*i)
    cur.close()
    return f'Все ошибки за {calendar.month_name[int(month)]} - {Counter(res_list).most_common()}' \
           f'\nИз них ночные(с 00:00 до 07:00) - {Counter(night_list).most_common()}'


def db_who_is_most_broken_off_all_time():
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("SELECT robot FROM robot_error")
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return Counter(res_list).most_common()


def db_who_fixed_the_most_off_all_time():
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("SELECT who_repair FROM robot_error")
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return Counter(res_list).most_common()


def db_who_fixed_in_current_month(month):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    first_day = datetime.today().replace(day=1).strftime('%Y-' + '0' + str(month) + '-%d')
    plus_month = datetime.today().replace(day=1, month=(int(month) + 1))
    last_day = plus_month - timedelta(days=1)
    cur.execute("SELECT who_repair FROM robot_error WHERE date BETWEEN :date1 AND :date2",
                {'date1': first_day, 'date2': last_day.strftime('%Y-%m-%d')})
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return Counter(res_list).most_common()



if __name__ == '__main__':
    print(db_who_is_most_broken_in_current_month("11"))
    print(db_who_fixed_in_current_month(10))