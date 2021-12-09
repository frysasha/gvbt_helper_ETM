import telebot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from telebot import apihelper
from funcbot import *
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Updater, Filters, ConversationHandler
from settingsbot import *
from proverkawhile import *


bot = telebot.TeleBot(TG_TOKEN)

def main():
    start('Старт бота был в ' + nowtimedate) #запись в лог о старте
    my_bot = Updater(TG_TOKEN, use_context=True) #обьявление бота
    #replykeyboard = telebot.types.ReplyKeyboardMarkup(True, False)  # кнопка снизу клавы
    #replykeyboard.row('LAPS', 'Pause', 'Work')
    welcome_message(bot) #временное сообщение для открытия клавы внизу
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('LAPS'), laps_start)],
                                                      states={
                                                          'user_name': [MessageHandler(Filters.text, laps_zapros)]},
                                                      fallbacks=[])) #реакция на LAPS , и последующее общение
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('ASK_Pause'), ask_pause_button))
    # my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('ASK_Pause'), ask_pause_button)],
    #                                                    states={},
    #                                                    fallbacks=[]))
    # my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('ASK_Work'), ask_work_button)],
    #                          states={},
    #                          fallbacks=[]))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('ASK_Work'), ask_work_button))
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_button_pressed)) #реакция на нажатую кнопку "поправил"


    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()


