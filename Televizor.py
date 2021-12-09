import os.path
import time
import datetime


wms_backup_file_time = datetime.datetime.fromtimestamp(os.path.getmtime('U:\\cwms_etm.bak'))
print('Дата последнего изменения backup WMS  ' + wms_backup_file_time.strftime("%d.%m.%Y, %H:%M"))


today = time.strftime("%d.%m.%Y")

ask_backup_file = datetime.datetime.fromtimestamp(os.path.getmtime('W:\\' + today))

print('Дата последнего изменения backup ASK  ' + ask_backup_file.strftime("%d.%m.%Y, %H:%M"))