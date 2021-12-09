from socket import *
from time import sleep
import pyautogui
import os
import sys

sys.path.append('C:\\python\\lib')

from pywinauto import Application
from pywinauto import findwindows

HOST = ''
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
uServSock = socket(AF_INET,SOCK_DGRAM)
uServSock.bind(SOCKADDR)

path = 'Y:\\python\\ASK screenshots\\' #куда сохраняются скрины


def scr_yellow():
    try:

        mainwindow = findwindows.find_window(best_match='<Желтый>.Agent.R') #ищем окно по лучшем совпадению имени
        appmain = Application().connect(handle=mainwindow)
        try:
            manualwindow = findwindows.find_window(best_match='Manual Control( Желтый)')  # ищем окно по лучшем совпадению имени
            appman = Application().connect(handle=manualwindow)
            appman.window(handle=manualwindow).close()  # закрывает окно
        except Exception as e:
            print('нет окна manual')
        appmain.window(handle=mainwindow).set_focus() #фокус на окне
        sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(path + 'yellow.png')
        print('скрин желтого создан')
    except Exception as e:
        print(e)


def scr_blue():
    try:
        mainwindow = findwindows.find_window(best_match='<Синий (красный)>.Agent.R') #ищем окно по лучшем совпадению имени
        appmain = Application().connect(handle=mainwindow)
        try:
            manualwindow = findwindows.find_window(best_match='Manual Control( Синий(красный))')  # ищем окно по лучшем совпадению имени
            appman = Application().connect(handle=manualwindow)
            appman.window(handle=manualwindow).close()  # закрывает окно
        except Exception as e:
            print('нет окна manual')
        appmain.window(handle=mainwindow).set_focus() #фокус на окне
        sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(path + 'blue.png')
        print('скрин голубого создан')
    except Exception as e:
        print(e)


def scr_priem():
    try:
        mainwindow = findwindows.find_window(best_match='<Приемный>.Agent.R')  # ищем окно по лучшем совпадению имени
        appmain = Application().connect(handle=mainwindow)
        try:
            manualwindow = findwindows.find_window(best_match='Manual Control( Приемный)')  # ищем окно по лучшем совпадению имени
            appman = Application().connect(handle=manualwindow)
            appman.window(handle=manualwindow).close()  # закрывает окно
        except Exception as e:
            print('нет окна manual')
        appmain.window(handle=mainwindow).set_focus()  # фокус на окне
        sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(path + 'priem.png')
        print('скрин приема создан')
    except Exception as e:
        print(e)


def pause_button():
    pyautogui.click(844, 709)
    sleep(1)
    pyautogui.click(541, 431)


def work_button():
    pyautogui.click(964, 709)
    sleep(1)
    pyautogui.click(541, 431)


def perezagruzka():
    pyautogui.click(964, 709)
    sleep(1)
    pyautogui.click(541, 431)
    sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(path + 'perezagruzka.png')

while True:


    data,addr = uServSock.recvfrom(BUFSIZE)
    loc_data = data.decode('cp1251')

    if loc_data == 'yellow':
        print('yellow')
        scr_yellow()

    if loc_data == 'blue':
        print('blue')
        scr_blue()

    if loc_data == 'priem':
        print('priem')
        scr_priem()

    if loc_data == 'pause_button':
        print('pause_button')
        pause_button()

    if loc_data == 'work_button':
        print('work_button')
        work_button()

    if loc_data == 'perezagruzka':
        print('perezagruzka')
        perezagruzka()



uServSock.close()