import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from selenium.webdriver.common.by import By

from hetzner.secondary_functions.password_generator import password_generator
from hetzner.secondary_functions.name_generator import name_generator
from datetime import datetime
from hetzner.mails_reg.auth import auth
from hetzner.databases_manage.database_scripts import insert_new_to_base_accounts, insert_new_to_tournament_accounts
from hetzner.mails_reg.create_driver import create_driver


def creator_emails(driver, count, hetzner_acc, hetzner_password,
                   country, champ_club, europe_club, male_club, female_club):

    driver.get('https://konsoleh.hetzner.com/mail.php/mailbox/create')
    try:
        for _ in range(count):
            driver.get('https://konsoleh.hetzner.com/mail.php/mailbox/create')
            WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.XPATH, '//form[@action="/mail.php/mailbox/create"]')))

            while True:
                mailbox_name = name_generator()
                password = password_generator()
                break

            driver.find_element(by=By.XPATH, value='//input[@id="localaddress_input"]').send_keys(mailbox_name)
            driver.find_element(by=By.XPATH, value='//input[@id="password_input"]').send_keys(password)
            driver.find_element(by=By.XPATH, value='//input[@id="password_repeat_input"]').send_keys(password)
            driver.find_element(by=By.XPATH, value='//input[@value="Save"]').click()
            insert_new_to_base_accounts(mailbox_name + "@sportmail.net", password,
                                        country, champ_club, europe_club, male_club, female_club)
            insert_new_to_tournament_accounts(mailbox_name + "@sportmail.net",
                                              password, country, champ_club, europe_club, male_club, female_club)
            try:
                result = driver.find_element(by=By.XPATH, value='//div[@class="ok"]').text
                expected_result = f"The mailbox '{mailbox_name}' was successfully created."
                print(expected_result)
            except NoSuchElementException:
                print("-" * 80)
                now = datetime.now()
                current_time = now.strftime("%H_%M_%S")
                print(current_time, "Strange error...")
                print("-" * 80)
            time.sleep(1.5)

        driver.close()
        driver.quit()
        print("Process Ended")

    except TimeoutException:
        auth(driver, hetzner_acc, hetzner_password)
        creator_emails(driver, count, hetzner_acc, hetzner_password,
                       country, champ_club, europe_club, male_club, female_club)
