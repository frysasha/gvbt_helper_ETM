import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from db import db_get_last_6_months, db_who_is_most_broken_in_current_month, \
    db_robot_stat_30_days, db_ask_cell_stat
from funcbot import create_csv_report, bot_mes

HOME_MENU, STAT_MENU, COMMANDS_MENU, SCHEDULE_MENU, SCHEDULE_UPLOAD_MENU, ASK_STAT_MONTH_MENU, ROBOT_MENU, \
CELL_STAT_MENU, SCHEDULE_MONTH_MENU = range(9)


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
        InlineKeyboardButton("По роботам(30 дн)", callback_data='ASK_robot_menu'),
        InlineKeyboardButton("По ячейкам", callback_data='ASK_cell_stat_menu'),
        InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    ask_stat_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_stat_menu_list, n_cols=3))
    query.edit_message_text(
        text="Выбери статистику", reply_markup=ask_stat_menu_keyboard
    )
    return STAT_MENU


def ask_cell_stat_menu(update, _):
    query = update.callback_query
    query.answer()
    ask_cell_stat_menu_list = [
        InlineKeyboardButton("По дате", callback_data='date'),
        InlineKeyboardButton("По ячейке", callback_data='section_error'),
        InlineKeyboardButton("Домой", callback_data='home_menu'),
    ]
    ask_cell_stat_menu_keyboard = InlineKeyboardMarkup(build_menu(ask_cell_stat_menu_list, n_cols=2))
    query.edit_message_text(
        text="Выбери сортировку", reply_markup=ask_cell_stat_menu_keyboard)
    return CELL_STAT_MENU


def ask_cell_stat_choice(update, context):
    query = update.callback_query
    query.answer()
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=open(create_csv_report(db_ask_cell_stat, query.data), 'rb'))
    return CELL_STAT_MENU


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
    query.edit_message_text(str(db_who_is_most_broken_in_current_month(query.data)),
                            reply_markup=ask_month_stat_menu_keyboard)
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
    second_month = str('0' + str(int(time.strftime("%m")) + 1)) if int(time.strftime("%m")) < 10 else int(
        time.strftime("%m")) + 1
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
    who_upload = update.message.chat.first_name
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download('S:\\09.ГВБТ\\Расписание\\' + selected_month + '.jpg')
    update.message.reply_text(text="Расписание загружено")
    bot_mes(f'{who_upload} загрузил новое расписание. Месяц - {selected_month}')
    print(f"{who_upload} загрузил новое расписание. Месяц - {selected_month}")
    return ConversationHandler.END


def schedule_show(update, context):
    query = update.callback_query
    query.answer()
    path = 'S:\\09.ГВБТ\\Расписание\\'
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path + time.strftime('%m') + '.jpg', 'rb'))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Нет расписания на текущий месяц')
    return SCHEDULE_MENU

def wrong_content_file(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Неправильный формат. Нужно отправить картинку')

