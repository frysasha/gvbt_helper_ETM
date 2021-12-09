
from selenium import webdriver
import time
from glob import glob
import os
from funcbot import *
from settingsbot import bot
import re


def firefox_update86():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-41183-firefox-esr.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_1') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    ffvers = open('C:\\python\\autodownload\\ffvers86.txt', 'r') #открывает с правами просмотра
    ffversread = ffvers.read()
    print("Firefox86 версия в файле ", ffversread)
    print("Firefox86 версия на сайте", version.text)

    if version.text == ffversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        ffvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for ff in glob("//172.29.30.3/dst/autodownload/*" + ffversread + "*"):
                print(ffversread)
                print('найден файл с версией ', ffversread, ff)
                os.remove(ff)
                print('файл' + ff + 'удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(80)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = ffversread
        new_vers = ffversread.replace(old_vers, versiontext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\ffvers86.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "x86Firefox", versiontext)
        print('изменил версию в файле')
        ffvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#firefox_update()

def firefox_update64():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-41183-firefox-esr.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_4') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    ffvers = open('C:\\python\\autodownload\\ffvers64.txt', 'r') #открывает с правами просмотра
    ffversread = ffvers.read()
    print("Firefox64 версия в файле ", ffversread)
    print("Firefox64 версия на сайте", version.text)

    if version.text == ffversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        ffvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for ff in glob("//172.29.30.3/dst/autodownload/*" + ffversread + "*x64*"):
                print(ffversread)
                print('найден файл с версией ', ffversread, ff)
                os.remove(ff)
                print('файл' + ff + 'удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(80)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = ffversread
        new_vers = ffversread.replace(old_vers, versiontext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\ffvers64.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "x64Firefox", versiontext)
        print('изменил версию в файле')
        ffvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#firefox_update64()

def skype_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-2663-skype.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_1') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    cleantext2 = version.text[:0] + version.text[:10] #убирается все кроме первых 10 символов
    cleantext = re.sub(r'\s', '', cleantext2) #убираются пробелы
    versiontext = version.text
    skypevers = open('C:\\python\\autodownload\\skypevers.txt', 'r') #открывает с правами просмотра
    skypeversread = skypevers.read()
    print("Skype версия в файле ", skypeversread)
    print("Skype версия на сайте", cleantext)

    if skypeversread == cleantext: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        skypevers.close() #закрывается файл txt
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for skype in glob("//172.29.30.3/dst/autodownload/*" + skypeversread + "*"): #ищется файл по части имени (версии программы)
                print('найден файл с версией ', skypeversread, skype)
                os.remove(skype) #удаляется файл(ы) если был найден по части имени
                print('файл ' + skype + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(80)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = skypeversread
        new_vers = skypeversread.replace(old_vers, cleantext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\skypevers.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "Skype", cleantext) #отправка в телегу сообщения
        print('изменил версию в файле')
        skypevers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#skype_update()

def cristaldisk_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-6420-crystaldiskinfo.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_1') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    cleantext = versiontext.replace('.', '_')
    crdvers = open('C:\\python\\autodownload\\crdvers.txt', 'r') #открывает с правами просмотра
    crdversread = crdvers.read()
    print("Cristal Disk версия в файле ", crdversread)
    print("Cristal Disk версия на сайте", cleantext)

    if cleantext == crdversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        crdvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for crd in glob("//172.29.30.3/dst/autodownload/*" + crdversread + "*"):
                print('найден файл с версией ', crdversread, crd)
                os.remove(crd)
                print('файл ' + crd + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(30)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = crdversread
        new_vers = crdversread.replace(old_vers, cleantext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\crdvers.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "Crystal Disk", cleantext)
        print('изменил версию в файле')
        crdvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#cristaldisk_update()

def zip_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-63-7-zip.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_4') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    cleantext = versiontext.replace('.', '')
    zipvers = open('C:\\python\\autodownload\\7zipvers.txt', 'r') #открывает с правами просмотра
    zipversread = zipvers.read()
    print("7Zip версия в файле ", zipversread)
    print("7Zip версия на сайте", cleantext)

    if cleantext == zipversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        zipvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for zp in glob("//172.29.30.3/dst/autodownload/*" + zipversread + "*"):
                print('найден файл с версией ', zipversread, zp)
                os.remove(zp)
                print('файл ' + zp + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(20)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = zipversread
        new_vers = zipversread.replace(old_vers, cleantext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\7zipvers.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "7Zip", cleantext)
        print('изменил версию в файле')
        zipvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#zip_update()

def cc_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-3151-ccleaner.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_2') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    cleantext2 = version.text[:0] + version.text[:4]  # убирается все кроме первых 10 символов
    cleantext = cleantext2.replace('.', '')  # убираются пробелы
    ccvers = open('C:\\python\\autodownload\\ccvers.txt', 'r') #открывает с правами просмотра
    ccversread = ccvers.read()
    print("Ccleaner версия в файле ", ccversread)
    print("Ccleaner версия на сайте", cleantext)

    if cleantext == ccversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        ccvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for ccl in glob("//172.29.30.3/dst/autodownload/*" + ccversread + "*"):
                print('найден файл с версией ', ccversread, ccl)
                os.remove(ccl)
                print('файл ' + ccl + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(50)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = ccversread
        new_vers = ccversread.replace(old_vers, cleantext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\ccvers.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "Ccleaner", cleantext)
        print('изменил версию в файле')
        ccvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')

#cc_update()

def tvnc_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-23148-tightvnc.html') #зайти на страницу
    link = browser.find_element_by_id('dl_link_4') #найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for') #находит версию на сайте
    versiontext = version.text
    tvncvers = open('C:\\python\\autodownload\\tvncvers.txt', 'r') #открывает с правами просмотра
    tvncversread = tvncvers.read()
    print("Tigth VNC версия в файле ", tvncversread)
    print("Tigth VNC версия на сайте", version.text)

    if version.text == tvncversread: #если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        tvncvers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else: #если версия в файле НЕ равно сервии на сайте
        try:
            for tvnc in glob("//172.29.30.3/dst/autodownload/*" + tvncversread + "*"):
                print('найден файл с версией ', tvncversread, tvnc)
                os.remove(tvnc)
                print('файл ' + tvnc + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(20)  # время для скачки файла
        #проверка скачки вайла нужна!
        old_vers = tvncversread
        new_vers = tvncversread.replace(old_vers, versiontext) #что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\tvncvers.txt', 'w') #открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers) #записать новую версию в файл
        update_message(bot, "Tigth VNC", versiontext)
        print('изменил версию в файле')
        tvncvers.close()
        try:
            browser.close()
            time.sleep(1)
            print('Проверка закончена')
        except:
            print('браузер недоступен')

#tvnc_update()

def google_update86():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-7868-google-chrome.html')  # зайти на страницу
    link = browser.find_element_by_id('dl_link_1')  # найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for')  # находит версию на сайте
    versiontext = version.text
    googlevers = open('C:\\python\\autodownload\\google86.txt', 'r')  # открывает с правами просмотра
    googleversread = googlevers.read()
    print("Google chrome x86 версия в файле ", googleversread)
    print("Google chrome x86 версия на сайте", version.text)

    if version.text == googleversread:  # если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        googlevers.close()
        try:
            browser.close()
            time.sleep(1)
            print('Проверка закончена')
        except:
            print('браузер недоступен')
    else:  # если версия в файле НЕ равно сервии на сайте
        try:
            for tvnc in glob("//172.29.30.3/dst/autodownload/ChromeStandaloneSetup*"):
                print('найден файл с версией ', googleversread, tvnc)
                os.remove(tvnc)
                print('файл ' + tvnc + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(100)  # время для скачки файла
        # проверка скачки вайла нужна!
        old_vers = googleversread
        new_vers = googleversread.replace(old_vers, versiontext)  # что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\google86.txt', 'w')  # открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers)  # записать новую версию в файл
        update_message(bot, "Google chrome x86", versiontext)
        print('изменил версию в файле')
        googlevers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
#google_update86()

def google_update64():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/get-7868-google-chrome.html')  # зайти на страницу
    link = browser.find_element_by_id('dl_link_2')  # найти ссылку скачивания
    version = browser.find_element_by_class_name('soft-name-for')  # находит версию на сайте
    versiontext = version.text
    googlevers = open('C:\\python\\autodownload\\google64.txt', 'r')  # открывает с правами просмотра
    googleversread = googlevers.read()
    print("Google chrome x64 версия в файле ", googleversread)
    print("Google chrome x64 версия на сайте", version.text)

    if version.text == googleversread:  # если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        googlevers.close()
        try:
            browser.close()
            time.sleep(1)
        except:
            print('браузер недоступен')
    else:  # если версия в файле НЕ равно сервии на сайте
        try:
            for tvnc in glob("//172.29.30.3/dst/autodownload/ChromeStandaloneSetup64*"):
                print('найден файл с версией ', googleversread, tvnc)
                os.remove(tvnc)
                print('файл ' + tvnc + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        link.click()  # кликнуть на ссылку
        time.sleep(100)  # время для скачки файла
        # проверка скачки вайла нужна!
        old_vers = googleversread
        new_vers = googleversread.replace(old_vers, versiontext)  # что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\google64.txt', 'w')  # открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers)  # записать новую версию в файл
        update_message(bot, "Google chrome x64", versiontext)
        print('изменил версию в файле')
        googlevers.close()
        try:
            browser.close()
            time.sleep(1)
            print('Проверка закончена')
        except:
            print('браузер недоступен')
#google_update64()

def zoom_update():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory":
        r"\\172.29.30.3\dst\autodownload"}  # убрать опцию безопасности, установить дефолтное место загрузки
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('C:\\python\\autodownload\\chromedriver.exe',
                               chrome_options=chromeOptions)  # указание вебдрайвера и запуска браузера с опцией
    browser.get('https://www.softportal.com/software-46881-zoom.html')  # зайти на страницу
    version = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/div/div[3]/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/span')  # находит версию на сайте
    versiontext = version.text
    zoomvers = open('C:\\python\\autodownload\\zoomvers.txt', 'r')  # открывает с правами просмотра
    zoomversread = zoomvers.read()
    print("Zoom версия в файле ", zoomversread)
    print("Zoom версия на сайте", version.text)

    if version.text == zoomversread:  # если версия в файле равна версии на сайте
        print('такая версия уже скачана')
        zoomvers.close()
        try:
            browser.close()
            time.sleep(1)
            print('Проверка закончена')
        except:
            print('браузер недоступен')
    else:  # если версия в файле НЕ равно сервии на сайте
        try:
            for tvnc in glob("//172.29.30.3/dst/autodownload/ZoomInstaller*"):
                print('найден файл с версией ', zoomversread, tvnc)
                os.remove(tvnc)
                print('файл ' + tvnc + ' удален')
        except:
            print('ошибка')
        print('найдена новая версия. скачиваю')
        browser.get('https://www.softportal.com/getsoft-46881-zoom-100.html')  # найти ссылку скачивания
        time.sleep(30)  # время для скачки файла
        # проверка скачки вайла нужна!
        old_vers = zoomversread
        new_vers = zoomversread.replace(old_vers, versiontext)  # что на что поменять
        write_new_vers = open('C:\\python\\autodownload\\zoomvers.txt', 'w')  # открыть с правами записи
        write_new_vers = write_new_vers.write(new_vers)  # записать новую версию в файл
        update_message(bot, "Zoom", versiontext)
        print('изменил версию в файле')
        zoomvers.close()
        try:
            browser.close()
            time.sleep(1)
            print('Проверка закончена')
        except:
            print('браузер недоступен')
#zoom_update()