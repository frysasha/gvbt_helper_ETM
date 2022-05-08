import telebot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from telebot import apihelper
from funcbot import *
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters, ConversationHandler, \
    CallbackContext
from settingsbot import *
from proverkawhile import *
from admin_panel import ask_stat_menu, ask_commands_menu, schedule_menu, home_menu, HOME_MENU, STAT_MENU, COMMANDS_MENU, \
    SCHEDULE_MENU, ask_month_stat_menu, ASK_STAT_MONTH_MENU, ask_month_choice, ask_robot_menu, ROBOT_MENU, \
    ask_robot_choice, \
    SCHEDULE_UPLOAD_MENU, schedule_month_menu, SCHEDULE_MONTH_MENU, schedule_month_choice, schedule_upload, \
    schedule_show

bot = telebot.TeleBot(TG_TOKEN)


def main():
    print('Старт бота был в ' + nowtimedate)  # запись в лог о старте
    my_bot = Updater(TG_TOKEN, use_context=True)  # обьявление бота
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('LAPS'), laps_start)],
                                                      states={
                                                          'user_name': [MessageHandler(Filters.text, laps_zapros)]},
                                                      fallbacks=[]))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК Пауза'), ask_pause_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расписание ГВБТ'), schedule))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК в работу'), ask_work_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика поломок общая'), all_statistic_bot))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика починок'), all_statistic_gvbt))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика за текущий месяц'), month_statistic_bot))
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_popravil_button_pressed,
                                                       pattern='popravil'))  # реакция на нажатую кнопку "поправил"
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_reshenie_button_pressed, pattern='reshenie'))
    my_bot.dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.user([423057805, 237426192]) & Filters.regex('/Admin'), home_menu)],
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
                    MessageHandler(Filters.photo, schedule_upload)
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
        fallbacks=[MessageHandler(Filters.user([423057805, 237426192]) & Filters.regex('/Admin'), home_menu)]))

    # my_bot.dispatcher.add_error_handler(error_hand)
    try:
        def pol():
            my_bot.start_polling()
            my_bot.idle()

        pol()
    except Exception as e:
        print('e')
        sleep(10)
        pol()


if __name__ == "__main__":
    # welcome_message(bot)
    main()
