from socket import *
from time import sleep
import pyautogui
import os
import sys
from pywinauto.application import Application
import cv2
import numpy as np
import threading


sys.path.append('C:\\python\\lib')

from pywinauto import Application
from pywinauto import findwindows

HOST = '172.29.30.63'
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
uServSock = socket(AF_INET,SOCK_DGRAM)
uCliSock = socket(AF_INET, SOCK_DGRAM)
uServSock.bind(SOCKADDR)

path = 'Y:\\python\\ASK screenshots\\' #куда сохраняются скрины


x = 0#координаты галки
y = 0


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
    sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(path + 'pause.new.png')

def work_button():
    pyautogui.click(964, 709)
    sleep(1)
    pyautogui.click(541, 431)
    sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(path + 'work.new.png')

def perezagruzka():
    pyautogui.click(964, 709)
    sleep(1)
    pyautogui.click(541, 431)
    sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(path + 'perezagruzka.png')


def resolv_robot_error():
    pyautogui.click(x, y)
    sleep(1)
    pyautogui.click(929, 176)#To resolve problem
    sleep(1)
    pyautogui.click(506, 431)#координаты ДА или ОК
    sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(path + 'resolve.png')

def check_upd():
    while True:
        data, addr = uServSock.recvfrom(BUFSIZE)
        loc_data = data.decode('cp1251')
        if loc_data == 'yellow':
            print('yellow')
            scr_yellow()
        elif loc_data == 'blue':
            print('blue')
            scr_blue()
        elif loc_data == 'priem':
            print('priem')
            scr_priem()
        elif loc_data == 'pause_button':
            print('pause_button')
            pause_button()
        elif loc_data == 'work_button':
            print('work_button')
            work_button()
        elif loc_data == 'perezagruzka':
            print('perezagruzka')
            perezagruzka()
        elif loc_data == 'Решить ошибку':
            resolv_robot_error()
        else:
            print('Неизвестная команда по UDP')

def check_galka():
    screenshot = pyautogui.screenshot()
    screenshot.save(path +'check_galka.png')
    img_rgb = cv2.imread(path +'check_galka.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(path + 'galka.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)

    res = (list(zip(*loc[::-1])))
    if res:
        x = res[0][0] + 5
        y = res[0][1] + 5
        print(f'галка по координатам {x= }{y= }')
        if 665 < x < 675 and 87 < y < 128:
            print('Допустимые координаты галки')
            uCliSock.sendto(bytes('Есть решение', 'cp1251'), SOCKADDR)
        else:
            print('Координаты галки недопустимые')
    else:
        print('Нет')



thread1 = threading.Timer(1, check_upd)
thread2 = threading.Timer(1, check_galka)

if __name__ == '__main__':
    print('Начало работы')
    thread1.start()
    thread2.start()




uServSock.close()