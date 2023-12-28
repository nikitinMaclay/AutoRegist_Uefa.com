import datetime
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.common.exceptions import NoSuchElementException

from uefa.uefa_site_reg.code_receiving import mail_getting
from hetzner.databases_manage.database_scripts import update_on_uefa_status, filling_clubs_table, get_all_countries, \
    delete_some_country
from uefa.uefa_site_reg.site_reg_func import driver_initialisation


def site_login_func(mail, password, link):
    driver = driver_initialisation()
    driver_waiting: WebDriverWait = WebDriverWait(driver, 30)

    driver.get(link)

    accept_cookies_btn = driver_waiting.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    accept_cookies_btn.click()
    login_btn = driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME, "nav-login__button")))
    login_btn.click()

    email_input = driver_waiting.until(EC.visibility_of_element_located((
        By.XPATH, '//*[@id="gigya-loginID-75579930407612940"]')))
    email_input.send_keys(mail)

    password_input = driver_waiting.until(EC.visibility_of_element_located((
        By.XPATH, '//*[@id="gigya-password-32665041627364124"]')))
    password_input.send_keys(password)

    time.sleep(2)

    send_btn = driver_waiting.until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="gigya-login-form"]/div[4]/div')))
    send_btn.click()

    acc_btn = driver_waiting.until(EC.element_to_be_clickable((By.XPATH,
                                                               '/html/body/div[4]/header/nav/div/ul/li[6]/div[2]')))
    acc_btn.click()

    your_teams_btn =\
        driver_waiting.until(EC.element_to_be_clickable((By.XPATH,
                                                         '//*[@id="idp-modal-wrapper"]/div/div/div[1]/div/nav/div[2]')))

    your_teams_btn.click()

    male_league_btn = driver_waiting.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="gigya-fan-preferences-teams-screen"]/div/div[2]/div[1]/div[2]/div')))

    male_league_btn.click()
    time.sleep(3)

    country_input = driver_waiting.until(EC.visibility_of_element_located((By.XPATH,
                                                                           '//*[@id="gigya-fan-preferences-teams-screen"]/div/div[2]/div[1]/div/div[1]/input')))
    data = get_all_countries()
    print(data)
    for el in data:
        country_input.send_keys(el['value'])
        time.sleep(6)
        try:
            no_result_status = driver.find_element(By.CLASS_NAME, value="no-result")
            delete_some_country(el['value'])
        except:
            pass
        country_input.clear()
    # club_name_input = driver_waiting.until(EC.visibility_of_element_located((
    #     By.XPATH, '//*[@id="gigya-fan-preferences-clubs-screen"]/div/div[2]/div[1]/div/div/div[1]/input')))
    # club_name_input.send_keys("HJK Helsinki")
    #
    # time.sleep(2)
    #
    # champions_league_clubs = driver.find_element(by=By.CLASS_NAME, value="idp-sayt-grid__dropdown--item")
    #
    # champions_league_clubs.click()

    # champions_league_clubs = driver.find_elements(by=By.CLASS_NAME, value="idp-sayt-grid__dropdown--item")
    #
    # clubs_names = [i.text.replace("d'Escaldes", "") for i in champions_league_clubs]
    # print(clubs_names)
    # filling_clubs_table(clubs_names, "champions_league")

    time.sleep(200)


# site_login_func("spears_BORSON92@sportmail.net", "=gvA.SfaI(iwdk?4A!4b", "https://uefa.com/")