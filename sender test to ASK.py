
from socket import *
import sys


HOST = '172.29.30.63'
HOST2 = '172.29.50.200'
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
SOCKADDR2 = (HOST2,PORT)

def send():
    uCliSock = socket(AF_INET,SOCK_DGRAM)
    uCliSock.sendto(bytes('Сформирован ежедневный отчет WMS. Необходимо проверить данные!', 'cp1251'), SOCKADDR)
    data, addr = uCliSock.recvfrom(BUFSIZE)
    uCliSock.close()

    return "OK"

send()