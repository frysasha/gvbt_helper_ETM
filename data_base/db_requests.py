import sqlite3
from datetime import date, timedelta, datetime
import calendar
from sqlalchemy import update, func, select, desc
from data_base.db import session
from data_base.tables.robot_error_table import RobotErrorTable


# cur = db1.cursor()
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
# db1.commit()


def db_error_insert(robot, date, time, cmd, section, faults):
    with section:
        request = RobotErrorTable(
            robot=robot,
            date=date,
            time=time,
            CMD_error=cmd,
            SECTION_error=section,
            faults=faults
        )
        session.add(request)
        session.commit()


def db_update_who_repair(who_repair):
    with session:
        request = update(RobotErrorTable).values(who_repair=who_repair).where(
            RobotErrorTable.ID.in_(session.query(func.max(RobotErrorTable.ID))))
        session.execute(request)
        session.commit()


def db_update_auto_repair():
    with session:
        request = update(RobotErrorTable).values(auto_repair='Да').where(
            RobotErrorTable.ID.in_(session.query(func.max(RobotErrorTable.ID))))
        session.execute(request)
        session.commit()


def db_who_is_most_broken_in_current_month(month: str):
    now_year = str(datetime.today().year)
    with session:
        request = session.query(RobotErrorTable.robot, func.count('*').label('count')).filter(
            func.strftime('%Y', RobotErrorTable.date) == now_year).filter(
            func.strftime('%m', RobotErrorTable.date) == month).group_by(RobotErrorTable.robot).order_by(desc("count"))
        night_errors = request.filter(RobotErrorTable.time.between('00:00:00', '07:00:00'))
        res_str = ''
        for i in request.all():
            res_str += f'{i.robot} - {i.count}\n'
        night_str = ''
        for i in night_errors.all():
            night_str += f'{i.robot} - {i.count}\n'
        return f'Все ошибки за {calendar.month_name[int(month)]} {now_year}:\n{res_str}' \
               f'\nИз них ночные(с 00:00 до 07:00):\n{night_str}'


def db_who_is_most_broken_off_all_time():
    with session:
        request = session.query(RobotErrorTable.robot, func.count('*').label('count')).group_by(
            RobotErrorTable.robot).order_by(desc('count'))
        str_res = ''
        for i in request.all():
            str_res += f'{i.robot} - {i.count}\n'
        return str_res


def db_who_fixed_the_most_off_all_time():
    with session:
        request = session.query(RobotErrorTable.who_repair, func.count('*').label('count')).group_by(
            RobotErrorTable.who_repair).order_by(desc('count'))
        str_res = ''
        for i in request.all():
            if i.who_repair is not None:
                str_res += f'{i.who_repair} - {i.count}\n'
        return str_res


def db_who_fixed_in_current_month(month):
    with session:
        request = session.query(RobotErrorTable.who_repair, func.count('*').label('count')).filter(
            func.strftime('%Y', RobotErrorTable.date) == str(datetime.today().year)).filter(
            func.strftime('%m', RobotErrorTable.date) == month).group_by(RobotErrorTable.who_repair).order_by(
            desc("count"))
        str_res = ''
        for i in request.all():
            if i.who_repair is not None:
                str_res += f'{i.who_repair} - {i.count}\n'
        return str_res


def db_who_win_in_prev_month(month):
    with session:
        request = session.query(RobotErrorTable.who_repair, func.count("*").label('count')).filter(
            func.strftime('%m', RobotErrorTable.date) == month).group_by(RobotErrorTable.who_repair).order_by(
            desc("count")).where(RobotErrorTable.who_repair.isnot(None))
        res = request.first()
        return f'{res.who_repair} - {res.count}'


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
    return f'{robot}:\nКоманда, Секция, Ошибка, Дата, Время\n{"=" * 45}\n{res_str}'


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
    # print(datetime.today().year)
    # print(db_ask_cell_stat('section_error'))
    # print(db_robot_stat_30_days('Желтый'))
    # print(db_who_is_most_broken_in_current_month("02"))
    # print(db_who_fixed_in_current_month("03"))
    # db_error_insert('Голубой', date=time.strftime("%Y-%m-%d"), time=time.strftime("%H:%M:%S"))
    # print(db_who_fixed_the_most_off_all_time())
    # print(db_who_win_in_prev_month('02'))
    # print(db_get_last_6_months())
    db_update_who_repair('z1232131111')
