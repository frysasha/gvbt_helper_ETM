from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from wms_user import get_user_list, wms_user_dict, del_user_from_wms, quit_browser_driver, browser_driver

HOME_MENU, WMS_MENU, WMS_USER_LIST_MENU, ARE_YOU_SURE_MENU = range(4)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def wms_menu(update, _):
    wms_menu_list = [
        InlineKeyboardButton("Список пользователей ТСД", callback_data='WMS_USER_LIST_MENU'),
        InlineKeyboardButton("Выйти", callback_data='exit'),
    ]
    menu_keyboard = InlineKeyboardMarkup(build_menu(wms_menu_list, n_cols=1))

    try:
        update.message.reply_text(
            text="Меню WMS", reply_markup=menu_keyboard
        )
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Меню WMS", reply_markup=menu_keyboard
        )
    return WMS_MENU

wms_user_list_query = None

def wms_user_list_menu(update, context):
    quit_browser_driver()
    query = update.callback_query
    query.answer()
    global wms_user_list_query
    wms_user_list_query = query
    query.edit_message_text(text="Загрузка...")
    user_list = get_user_list()
    if user_list == 'Нет активных пользователей ТСД':
        query.edit_message_text(text=user_list)
        quit_browser_driver()
        return ConversationHandler.END
    wms_usr_menu_list = [
        InlineKeyboardButton("Выйти", callback_data='exit'),
    ]
    menu_keyboard = InlineKeyboardMarkup(build_menu(wms_usr_menu_list, n_cols=1))
    query.edit_message_text(text=user_list, reply_markup=menu_keyboard)
    #query.edit_message_text(text="Введи номер пользователя")
    return WMS_USER_LIST_MENU


def are_you_sure_menu(update, context):

    if update.callback_query:
        query = update.callback_query
        query.answer(cache_time=5)
        wms_user_name = wms_user_dict[update.callback_query.data]
        del_user_from_wms(wms_user_name)
        query.edit_message_text(text=f'{wms_user_name} Удален', reply_markup='')
        return ConversationHandler.END
    else:
        wms_user_menu_list = [
            InlineKeyboardButton("Удалить из WMS", callback_data=int(update.message.text)),
            InlineKeyboardButton("Список пользователей ТСД", callback_data='WMS_USER_LIST_MENU'),
            InlineKeyboardButton("Выйти", callback_data='exit'),
        ]
        menu_keyboard = InlineKeyboardMarkup(build_menu(wms_user_menu_list, n_cols=1))
        try:
            wms_user_name = wms_user_dict[update.message.text]
            wms_user_list_query.edit_message_text(text=f"Удалить пользователя {wms_user_name}?", reply_markup=menu_keyboard)
            return ARE_YOU_SURE_MENU
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Пользователь {update.message.text} не найден")
            return WMS_USER_LIST_MENU


def wrong_number(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Необходимо ввести номер пользователя из списка!")
    return WMS_USER_LIST_MENU


def exit_from_wms_menu(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Выход', reply_markup='')
    quit_browser_driver()
    return ConversationHandler.END
