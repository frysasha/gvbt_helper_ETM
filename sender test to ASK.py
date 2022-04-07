
from socket import *
import sys


HOST = '172.29.30.63'
HOST2 = '172.29.50.200'
HOST3 = '172.29.2.125'
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
SOCKADDR2 = (HOST2,PORT)
SOCKADDR3 = (HOST3,PORT)

def send():
    uCliSock = socket(AF_INET,SOCK_DGRAM)
    uCliSock.sendto(bytes('Сформирован ежедневный отчет WMS. Необходимо проверить данные!', 'cp1251'), SOCKADDR)
    data, addr = uCliSock.recvfrom(BUFSIZE)
    uCliSock.close()


def send_robot_resolve():
    uCliSock = socket(AF_INET, SOCK_DGRAM)
    uCliSock.sendto(bytes('Желтый есть решение', 'cp1251'), SOCKADDR)
    data, addr = uCliSock.recvfrom(BUFSIZE)
    uCliSock.close()

def send_to_ASK():
    uCliSock = socket(AF_INET, SOCK_DGRAM)
    uCliSock.sendto(bytes('yellow', 'utf-8'), SOCKADDR3)
    data, addr = uCliSock.recvfrom(BUFSIZE)
    uCliSock.close()

if __name__ == '__main__':
    #send()
    #send_robot_resolve()
    send_to_ASK()