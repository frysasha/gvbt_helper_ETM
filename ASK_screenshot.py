# -*- encoding: utf-8 -*-

from socket import *
from time import sleep
import pyautogui
import os
import sys
import cv2
import numpy as np
import threading

sys.path.append('C:\\python\\lib')

HOST = ''
HOST2 = '172.29.30.63'
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST, PORT)
SOCKADDR2 = (HOST2, PORT)
uServSock = socket(AF_INET,SOCK_DGRAM)
uCliSock = socket(AF_INET, SOCK_DGRAM)
uServSock.bind(SOCKADDR)

PATH = 'Y:\\python\\ASK\\screenshots\\'

robot_error = False


PAUSE_BUTTON_COORDS = (844, 709)
WORK_BUTTON_COORDS = (964, 709)
ACCEPT_BUTTON_COORDS = (541, 431)
RESOLVE_PROBLEM_BUTTON_COORDS = (929, 176)
ACCEPT_RESOLVE_PROBLEM_COORDS = (534, 434)


def create_screenshot(filename):
    screenshot = pyautogui.screenshot()
    try:
        screenshot.save(PATH + filename + '.png')
    except Exception as e:
        print(e)
        print('Cannot save screenshot')
    print(filename + 'screen created')


def pause():
    pyautogui.click(PAUSE_BUTTON_COORDS)
    sleep(1)
    pyautogui.click(ACCEPT_BUTTON_COORDS)
    create_screenshot('pause')


def work():
    pyautogui.click(WORK_BUTTON_COORDS)
    sleep(1)
    pyautogui.click(ACCEPT_BUTTON_COORDS)
    create_screenshot('work')

def resolv_robot_error():
    print('najimau na koordinaty')
    print(x, y)
    pyautogui.click(x, y)
    sleep(1)
    pyautogui.click(RESOLVE_PROBLEM_BUTTON_COORDS)
    sleep(1)
    pyautogui.click(ACCEPT_RESOLVE_PROBLEM_COORDS)
    sleep(1)
    create_screenshot('resolve')
    robot_error = False


def check_galka():
    while True:
        screenshot = pyautogui.screenshot()
        screenshot.save(PATH +'check_galka.png')
        img_rgb = cv2.imread(PATH +'check_galka.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(PATH + 'galka.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        res = (list(zip(*loc[::-1])))
        if res:
            global x, y
            x = res[0][0] + 5
            y = res[0][1] + 5
            if 600 < x < 675 and 87 < y < 128:
                uCliSock.sendto(bytes('Est reshenie'), SOCKADDR2)
        sleep(1)


def check_upd():
    while True:
        data, addr = uServSock.recvfrom(BUFSIZE)
        loc_data = data
        if loc_data == 'robot_error':
            print(loc_data)
            robot_error = True
            create_screenshot('robot_error')
        elif loc_data == 'pause_button':
            print('pause_button')
            pause()
        elif loc_data == 'work_button':
            print('work_button')
            work()
        elif loc_data == 'Resolve problem':
            print(loc_data)
            resolv_robot_error()
        else:
            print('unknown command UDP')
        sleep(1)

thread1 = threading.Timer(1, check_upd)
thread2 = threading.Timer(1, check_galka)

if __name__ == '__main__':
    print('Nachalo raboty')
    thread1.start()
    thread2.start()
