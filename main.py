import telebot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from telebot import apihelper
from funcbot import *
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters, ConversationHandler, CallbackContext
from settingsbot import *
from proverkawhile import *
from db import db_who_is_most_broken_off_all_time


bot = telebot.TeleBot(TG_TOKEN)

def main():
    start('Старт бота был в ' + nowtimedate) #запись в лог о старте
    my_bot = Updater(TG_TOKEN, use_context=True) #обьявление бота
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('LAPS'), laps_start)],
                                                      states={
                                                          'user_name': [MessageHandler(Filters.text, laps_zapros)]},
                                                      fallbacks=[CommandHandler('cancel', ConversationHandler.END)])) #реакция на LAPS , и последующее общение
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК Пауза'), ask_pause_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расписание ГВБТ'), schedule))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('АСК в работу'), ask_work_button))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика поломок общая'), all_statistic_bot))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика починок'), all_statistic_gvbt))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Статистика за текущий месяц'), month_statistic_bot))
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_button_pressed)) #реакция на нажатую кнопку "поправил"
    my_bot.dispatcher.add_error_handler(error_handler)

    # my_bot.dispatcher.add_handler(CommandHandler('Schedule', schedule))
    # my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('ASK_Pause'), ask_pause_button)],
    #                                                    states={},
    #                                                    fallbacks=[]))
    # my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('ASK_Work'), ask_work_button)],
    #                          states={},
    #                          fallbacks=[]))

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
    #welcome_message(bot)
    #test_mes(bot)
    #month_statistic_gvbt(bot, '03')
    #wms_day_report_message(bot)
    main()



