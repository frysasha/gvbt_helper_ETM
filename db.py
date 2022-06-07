import sqlite3
from datetime import date, timedelta, datetime
import time
from collections import Counter
import calendar
#
# db = sqlite3.connect('robots.db')
# cur = db.cursor()
#
# cur.execute("""CREATE TABLE IF NOT EXISTS robot_error(
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#    robot TEXT,
#    date DATE,
#    time TIME,
#    who_repair TEXT,
#    auto_repair TEXT,
#    CMD_error TEXT,
#    SECTION_error TEXT,
#    faults TEXT);
# """)
# db.commit()


def db_error_insert(robot, date, time, cmd, section, faults):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("INSERT INTO robot_error (robot, date, time, CMD_error, SECTION_error, faults) VALUES (?, ?, ?, ?, ?, ?);",
                (robot, date, time, cmd, section, faults))
    db.commit()
    cur.close()


def db_update_who_repair(who_repair):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("UPDATE robot_error SET who_repair =:who WHERE ID = (SELECT MAX(ID) FROM robot_error)",
                {'who': who_repair})
    db.commit()
    cur.close()


def db_update_auto_repair():
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("UPDATE robot_error SET auto_repair ='Да' WHERE ID = (SELECT MAX(ID) FROM robot_error)")
    db.commit()
    cur.close()


def db_who_is_most_broken_in_current_month(month):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("SELECT robot FROM robot_error where strftime ('%m', date) = :month", {'month': month})
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.execute(
        "SELECT robot FROM robot_error WHERE (time BETWEEN '00:00:00' AND '07:00:00') AND strftime ('%m', date) = :month",
        {'month': month})
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
    cur.execute("SELECT who_repair FROM robot_error where who_repair is not null")
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return Counter(res_list).most_common()


def db_who_fixed_in_current_month(month):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("SELECT who_repair FROM robot_error WHERE strftime ('%m', date) = :month and who_repair is not null",
                {'month': month})
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return Counter(res_list).most_common()


def db_who_win_in_prev_month(month):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("""select who_repair, max(cnt)
                    from
                    (SELECT who_repair, count(*) as cnt
                    FROM robot_error 
                    WHERE strftime ('%m', date) = :month
                    group by who_repair)
                    where who_repair is not null""", {'month': month})
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(i)
    cur.close()
    return res_list


def db_get_last_6_months():
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("""Select distinct strftime('%m', date)
                from robot_error
                where date between date('now','-6 month') and date('now')""")
    res = cur.fetchall()
    res_list = []
    for i in res:
        res_list.append(*i)
    cur.close()
    return res_list


def db_robot_stat_30_days(robot):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute("""select CMD_error, SECTION_error, faults, date, time
                from robot_error
                where robot = :robot and CMD_error is not null
                and date between date('now','-30 day') and date('now')""", {"robot": robot})
    res = cur.fetchall()
    res_str = ''
    for i in res:
        res_str = res_str + str(i) + '\n'
    cur.close()
    return f'{robot}:\nКоманда, Секция, Ошибка, Дата, Время\n{"="* 45}\n{res_str}'

def db_ask_cell_stat(order_by):
    db = sqlite3.connect('robots.db')
    cur = db.cursor()
    cur.execute(f"""select  SECTION_error, cmd_error, robot, faults, date, time
                    from robot_error
                    where CMD_error is not null
                    and date between date('now','-1 year') and date('now')
                    order by {order_by}""")
    res = cur.fetchall()
    res_str = ''
    for i in res:
        res_str = res_str + str(i) + '\n'
    cur.close()
    return res

if __name__ == '__main__':
    print(db_ask_cell_stat('section_error'))
    #print(db_robot_stat_30_days('Желтый'))
    # print(db_who_is_most_broken_in_current_month("11"))
    # print(db_who_fixed_in_current_month(10))
    # db_error_insert('Голубой', date=time.strftime("%Y-%m-%d"), time=time.strftime("%H:%M:%S"))
