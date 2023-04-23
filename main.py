import telebot
from telegram.ext import CallbackQueryHandler, MessageHandler, Updater, Filters, ConversationHandler

from telegram_bot.panels.admin_menu import ask_stat_menu, ask_commands_menu, schedule_menu, home_menu, HOME_MENU, STAT_MENU, COMMANDS_MENU, \
    SCHEDULE_MENU, ask_month_stat_menu, ASK_STAT_MONTH_MENU, ask_month_choice, ask_robot_menu, ROBOT_MENU, \
    ask_robot_choice, \
    SCHEDULE_UPLOAD_MENU, schedule_month_menu, SCHEDULE_MONTH_MENU, schedule_month_choice, schedule_upload, \
    schedule_show, CELL_STAT_MENU, ask_cell_stat_choice, ask_cell_stat_menu, wrong_content_file
from telegram_bot.panels.wms_user_menu import wms_menu, wms_user_list_menu, are_you_sure_menu, WMS_MENU, WMS_USER_LIST_MENU, \
    ARE_YOU_SURE_MENU, exit_from_wms_menu, wrong_number
from funcbot import laps_start, laps_zapros, ask_pause_button, schedule, ask_work_button, all_statistic_bot, \
    all_statistic_gvbt, month_statistic_bot, inline_popravil_button_pressed, inline_reshenie_button_pressed, show_cartridges, \
    start_bot_message_with_keyboards
from proverkawhile import main_threads
from settings import TG_TOKEN, nowtimedate, ADMIN_USERS_ID
from telegram.utils.request import NetworkError
from requests.adapters import ProxyError
from time import sleep


bot = telebot.TeleBot(TG_TOKEN)


def main():
    print('Старт бота был в ' + nowtimedate)
    my_bot = Updater(TG_TOKEN, use_context=True)
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('LAPS'), laps_start)],
                                                      states={
                                                          'user_name': [MessageHandler(Filters.text, laps_zapros)]},
                                                      fallbacks=[]))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК Пауза'), ask_pause_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расписание ГВБТ'), schedule))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК в работу'), ask_work_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Картриджи по принтерам'), show_cartridges))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика поломок общая'), all_statistic_bot))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика починок'), all_statistic_gvbt))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика за текущий месяц'), month_statistic_bot))
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_popravil_button_pressed,
                                                       pattern='popravil'))  # реакция на нажатую кнопку "поправил"
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_reshenie_button_pressed, pattern='reshenie'))
    my_bot.dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.user(ADMIN_USERS_ID) & Filters.regex('/Admin'), home_menu)],
        states={
            HOME_MENU:
                [
                    CallbackQueryHandler(ask_stat_menu, pattern='ASK_stat'),
                    CallbackQueryHandler(ask_commands_menu, pattern='ASK_commands'),
                    CallbackQueryHandler(schedule_menu, pattern='Schedule'),
                ],
            STAT_MENU:
                [
                    CallbackQueryHandler(home_menu, pattern='home_menu'),
                    CallbackQueryHandler(ask_month_stat_menu, pattern='ASK_month_stat'),
                    CallbackQueryHandler(ask_robot_menu,
                                         pattern='ASK_robot_menu'),
                    CallbackQueryHandler(ask_cell_stat_menu,
                                         pattern='ASK_cell_stat_menu'),
                ],
            CELL_STAT_MENU:
                [
                    CallbackQueryHandler(home_menu, pattern='home_menu'),
                    CallbackQueryHandler(ask_cell_stat_choice,
                                         pattern='date|section_error'),
                ],
            COMMANDS_MENU:
                [
                    CallbackQueryHandler(home_menu, pattern='home_menu'),
                    CallbackQueryHandler(ask_pause_button, pattern='ASK_pause'),
                    CallbackQueryHandler(ask_work_button, pattern='ASK_work'),
                ],
            SCHEDULE_MENU:
                [
                    CallbackQueryHandler(schedule_month_menu, pattern='schedule_upload_month_menu'),
                    CallbackQueryHandler(schedule_show, pattern='schedule_show'),
                    CallbackQueryHandler(home_menu, pattern='home_menu')
                ],
            SCHEDULE_UPLOAD_MENU:
                [
                    MessageHandler(Filters.photo, schedule_upload),
                    MessageHandler(~ Filters.photo, wrong_content_file)
                ],
            SCHEDULE_MONTH_MENU:
                [
                    CallbackQueryHandler(schedule_month_choice,
                                         pattern='[01-12]'),
                    CallbackQueryHandler(home_menu, pattern='home_menu')
                ],
            ASK_STAT_MONTH_MENU:
                [
                    CallbackQueryHandler(ask_month_choice, pattern='[01-12]'),
                    CallbackQueryHandler(home_menu, pattern='home_menu')
                ],
            ROBOT_MENU:
                [
                    CallbackQueryHandler(ask_robot_choice,
                                         pattern='Желтый|Голубой|Приемный'),
                    CallbackQueryHandler(home_menu, pattern='home_menu')
                ],
        },
        fallbacks=[MessageHandler(Filters.user(ADMIN_USERS_ID) & Filters.regex('/Admin'), home_menu)]))

    my_bot.dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('/WMS'), wms_menu)],
        states={
            WMS_MENU:
                [
                    CallbackQueryHandler(wms_user_list_menu, pattern='WMS_USER_LIST_MENU'),
                    CallbackQueryHandler(exit_from_wms_menu, pattern='exit'),
                ],
            WMS_USER_LIST_MENU:
                [
                    CallbackQueryHandler(exit_from_wms_menu, pattern='exit'),
                    MessageHandler(Filters.regex(r'^[1-9][0-9]?$|^100$'), are_you_sure_menu),
                    MessageHandler(Filters.text, wrong_number),
                ],
            ARE_YOU_SURE_MENU:
                [
                    CallbackQueryHandler(wms_user_list_menu, pattern='WMS_USER_LIST_MENU'),
                    CallbackQueryHandler(exit_from_wms_menu, pattern='exit'),
                    CallbackQueryHandler(are_you_sure_menu, pattern=r'^[1-9][0-9]?$|^100$'),

                ],
        },
        fallbacks=[MessageHandler(Filters.user(ADMIN_USERS_ID) & Filters.regex('/WMS'), wms_menu)]
    ))

    #my_bot.dispatcher.add_error_handler(error_hand)
    def start():
        my_bot.start_polling(timeout=20, bootstrap_retries=5)
        my_bot.idle()
    try:
        start()
    except NetworkError:
        print('network error!!')
        sleep(2)
        start()
    except ProxyError:
        print('proxy error!!')
        sleep(2)
        start()


if __name__ == "__main__":
    start_bot_message_with_keyboards(bot)
    main_threads()
    main()

