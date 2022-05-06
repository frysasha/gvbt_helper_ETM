import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from db import db_get_last_6_months, db_who_is_most_broken_in_current_month, db_who_fixed_in_current_month, \
    db_robot_stat_30_days


HOME_MENU, STAT_MENU, COMMANDS_MENU, SCHEDULE_MENU, SCHEDULE_UPLOAD_MENU, ASK_STAT_MONTH_MENU, ROBOT_MENU, SCHEDULE_MONTH_MENU = range(8)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def home_menu(update, _):
    home_button_list = [
        InlineKeyboardButton("Статистика АСК", callback_data='ASK_stat'),
        InlineKeyboardButton("Команды АСК", callback_data='ASK_commands'),
        InlineKeyboardButton("Расписание", callback_data='Schedule')
    ]

    admin_keyboard = InlineKeyboardMarkup(build_menu(home_button_list, n_cols=2))
    try:
        update.message.reply_text(text="Меню Администратора", reply_markup=admin_keyboard)
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Меню Администратора", reply_markup=admin_keyboard)
    return HOME_MENU


def ask_stat_menu(update, _):
    query = update.callback_query
    query.answer()
    ask_stat_menu_list = [
            InlineKeyboardButton("За месяц", callback_data='ASK_month_stat'),
            InlineKeyboardButton("По роботам(30 дней)", callback_data='ASK_robot_menu'),
            InlineKeyboardButton("Домой", callback_data='home_menu'),
            ]
    ask_stat_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_stat_menu_list, n_cols=2))
    query.edit_message_text(
        text="Выбери статистику", reply_markup=ask_stat_menu_keyboard
    )
    return STAT_MENU


def ask_month_stat_menu(update, _):
    query = update.callback_query
    query.answer()
    ask_month_stat_menu_list = [
        InlineKeyboardButton(i, callback_data=i) for i in db_get_last_6_months()
    ]
    ask_month_stat_menu_list.append(InlineKeyboardButton("Домой", callback_data='home_menu'))
    ask_month_stat_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_month_stat_menu_list, n_cols=6))
    query.edit_message_text(
        text="Выбери месяц", reply_markup=ask_month_stat_menu_keyboard
    )
    return ASK_STAT_MONTH_MENU


def ask_month_choice(update, _):
    query = update.callback_query
    query.answer()
    ask_month_stat_menu_list = [
        InlineKeyboardButton(i, callback_data=i) for i in db_get_last_6_months()
    ]
    ask_month_stat_menu_list.append(InlineKeyboardButton("Домой", callback_data='home_menu'))
    ask_month_stat_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_month_stat_menu_list, n_cols=6))
    query.edit_message_text(str(db_who_is_most_broken_in_current_month(query.data)), reply_markup=ask_month_stat_menu_keyboard)
    return ASK_STAT_MONTH_MENU


def ask_robot_menu(update, _):
    query = update.callback_query
    query.answer()
    ask_robot_list = [
        InlineKeyboardButton("Желтый", callback_data='Желтый'),
        InlineKeyboardButton("Голубой", callback_data='Голубой'),
        InlineKeyboardButton("Приемный", callback_data='Приемный'),
        InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    ask_robot_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_robot_list, n_cols=3))
    query.edit_message_text(
        text="Выбери робота", reply_markup=ask_robot_menu_keyboard)
    return ROBOT_MENU


def ask_robot_choice(update, _):
    query = update.callback_query
    query.answer()
    ask_robot_list = [
        InlineKeyboardButton("Желтый", callback_data='Желтый'),
        InlineKeyboardButton("Голубой", callback_data='Голубой'),
        InlineKeyboardButton("Приемный", callback_data='Приемный'),
        InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    ask_robot_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_robot_list, n_cols=3))
    query.edit_message_text(str(db_robot_stat_30_days(query.data)), reply_markup=ask_robot_menu_keyboard)
    return ROBOT_MENU


def ask_commands_menu(update, _):
    query = update.callback_query
    query.answer()
    ask_commands_menu_list = [
            InlineKeyboardButton("АСК Пауза 🤖", callback_data='ASK_pause'),
            InlineKeyboardButton("АСК в работу 🤖", callback_data='ASK_work'),
            InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    ask_commands_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_commands_menu_list, n_cols=2))
    query.edit_message_text(
        text="Выбери команду", reply_markup=ask_commands_menu_keyboard
    )
    return COMMANDS_MENU


def schedule_menu(update, _):
    query = update.callback_query
    query.answer()
    schedule_menu_list = [
            InlineKeyboardButton("Текущее расписание", callback_data='schedule_show'),
            InlineKeyboardButton("Загрузить расписание", callback_data='schedule_upload_month_menu'),
            InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    schedule_menu_keyboard = InlineKeyboardMarkup(build_menu(schedule_menu_list, n_cols=2))
    query.edit_message_text(
        text="Выбери расписание", reply_markup=schedule_menu_keyboard)
    return SCHEDULE_MENU


def schedule_month_menu(update, _):
    query = update.callback_query
    query.answer()
    current_month = time.strftime("%m")
    second_month = str('0' + str(int(time.strftime("%m")) + 1)) if int(time.strftime("%m")) < 10 else int(time.strftime("%m")) + 1
    schedule_month_menu_list = [
        InlineKeyboardButton(current_month, callback_data=time.strftime("%m")),
        InlineKeyboardButton(second_month, callback_data=second_month),
        InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    schedule_month_menu_keyboard = InlineKeyboardMarkup(build_menu(schedule_month_menu_list, n_cols=2))
    query.edit_message_text(
        text="Выбери месяц", reply_markup=schedule_month_menu_keyboard)
    return SCHEDULE_MONTH_MENU


def schedule_month_choice(update, _):
    query = update.callback_query
    query.answer()
    global selected_month
    selected_month = query.data
    query.edit_message_text(
        text="Загрузи картинку расписания", reply_markup='')
    return SCHEDULE_UPLOAD_MENU


def schedule_upload(update, context):

    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download('Z:\\python\\расписание\\' + selected_month + '.jpg')
    update.message.reply_text(text="Расписание загружено")
    print("загрузили новое расписание" + selected_month)
    return ConversationHandler.END


def schedule_show(update, context):
    query = update.callback_query
    query.answer()
    path = 'Z:\\python\\расписание\\'
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path + time.strftime('%m') + '.jpg', 'rb'))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Нет расписания на текущий месяц')
    return SCHEDULE_MENU