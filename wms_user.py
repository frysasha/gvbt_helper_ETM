from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WMS_OHE_AUTH_URL = r'http://172.29.2.26/cwms/(S(rfgzla3vve5nxvgbm1kwqx5r))/OheWebReports.aspx'
USER_AUTH_LOGIN = '09shai'
USER_AUTH_PASSWORD = '1337'

wms_user_dict = {}
browser_driver = None


def get_browser_driver():
    print('Страрт браузера')
    profile = webdriver.FirefoxProfile()
    binary = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    profile.set_preference("browser.preferences.instantApply", True)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)

    return driver


def get_user_list():
    global browser_driver
    global wms_user_dict
    wms_user_dict.clear()
    user_list_str = ''
    driver = get_browser_driver()
    driver.minimize_window()
    browser_driver = driver
    wait = WebDriverWait(driver, 30)
    driver.get(WMS_OHE_AUTH_URL)
    driver.implicitly_wait(15)
    login = driver.find_element(By.ID, 'USR')
    password = driver.find_element(By.ID, 'PSD')
    login.send_keys(USER_AUTH_LOGIN)
    password.send_keys(USER_AUTH_PASSWORD)
    submit_button = driver.find_element(By.CSS_SELECTOR, '#sbm > span')
    submit_button.click()
    admin_panel_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="csadminpanels"]/span[1]')))
    admin_panel_button.click()
    user_control_button = wait.until(EC.element_to_be_clickable((By.ID, 'ui-id-17')))
    user_control_button.click()
    try:
        no_users = driver.find_element(By.CSS_SELECTOR, '#tabs-1 > p:nth-child(1)')
        return 'Нет активных пользователей ТСД'
    except:

        elements_usr_list = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="tlnusers"]/tbody/tr')))
        for id, element in enumerate(elements_usr_list):
            if id > 0:
                wms_user_dict[str(id)] = element.get_attribute('id')
                user_list_str += f"{id}. {element.get_attribute('id')}\n"

        return user_list_str



def del_user_from_wms(user_name):
    if browser_driver:
        print('Удаляю из WMS ', user_name)
        user_checkbox = browser_driver.find_element(By.ID, f'jqg_tlnusers_{user_name}')
        user_checkbox.click()
        del_button = browser_driver.find_element(By.ID, 'telnetmanage')
        del_button.click()
        quit_browser_driver()
    else:
        print(f'Не определен driver!')


def quit_browser_driver():
    if browser_driver:
        browser_driver.quit()
        print('Закрываю браузер')
    else:
        print(f'Не определен driver!')


if __name__ == '__main__':
    print(get_user_list())
