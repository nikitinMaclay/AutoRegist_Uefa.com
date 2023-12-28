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

api_key = "852752f593e1156cdad6b102e2764b6d"
solver = TwoCaptcha(api_key=api_key)


class DriverUndefinedException(Exception):
    def __init__(self, message="Driver is closed or has never been created"):
        self.message = message
        super().__init__(self.message)


class CodeUndefinedException(Exception):
    def __init__(self, message="Code hasn't been received"):
        self.message = message
        super().__init__(self.message)


def driver_initialisation():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    # profile_directory = r'%AppData%\Mozilla\Firefox\Profiles\z6l67q5o.uefa'
    # profile = webdriver.FirefoxProfile(os.path.expandvars(profile_directory))
    # options.profile = profile

    driver = webdriver.Chrome(options=options)

    return driver


def start_registration(accounts, link):

    for idx, account in enumerate(accounts):
        driver = driver_initialisation()
        driver_waiting: WebDriverWait = WebDriverWait(driver, 30)

        driver.get(link)

        accept_cookies_btn = driver_waiting.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies_btn.click()
        login_btn = driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME, "nav-login__button")))
        login_btn.click()

        new_account_btn = driver_waiting.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="gigya-login-form"]/div[4]/a')))
        new_account_btn.click()

        time.sleep(1.5)
        email_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-75074230944436030"]')))
        password_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-password-59919533498235100"]')))
        first_name_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-130722358975432270"]')))
        last_name_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-30497114450394400"]')))
        email_field.send_keys(account["mail"])
        time.sleep(0.7)
        password_field.send_keys(account["password"])
        time.sleep(0.7)
        first_name_field.send_keys(account["mail"].split("@")[0].split("_")[0])
        time.sleep(0.7)
        last_name_field.send_keys(account["mail"].split("@")[0].split("_")[-1])
        time.sleep(0.7)

        birth_day_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-88315185881230510"]')))
        birth_month_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-105406014904922500"]')))
        birth_year_field = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-32538633360993784"]')))

        birth_day_field.send_keys(random.choice(range(1, 30)))
        time.sleep(0.7)
        birth_month_field.send_keys(random.choice(range(1, 12)))
        time.sleep(0.7)
        birth_year_field.send_keys(random.choice(range(1975, 2005)))
        time.sleep(0.7)

        accept_terms_and_conditions_checkbox = driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-register-form"]/div[1]/div[11]/label/span')))

        driver.execute_script("arguments[0].click();", accept_terms_and_conditions_checkbox)

        create_account_btn = driver_waiting.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="gigya-register-form"]/div[1]/div[13]/input')))

        try:
            create_account_btn.click()
        except:
            driver.execute_script("arguments[0].click();", create_account_btn)

        time.sleep(1)
        driver.switch_to.default_content()

        try:

            captcha_iframe = driver_waiting.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[12]/div[2]/iframe')))

        except:
            try:
                captcha_iframe = driver_waiting.until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, "[title='recaptcha challenge expires in two minutes']")))
            except:
                pass

        try:
            captcha_url = captcha_iframe.get_attribute("src")
            captcha_sitekey = captcha_url.split("k=")[-1]
            result = solver.solve_captcha(captcha_sitekey, link)
            print(result)
            driver.execute_script(f"window.___grecaptcha_cfg.clients[0].A.A.callback('{result}')")
            time.sleep(1)
            actions = ActionChains(driver)
            actions.move_by_offset(100, 100).perform()
            actions.click().perform()
        except:
            pass
        time.sleep(3)
        try:
            confirmation_code_inputs = driver_waiting.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "idp-otp-login-pin")))

            confirmation_code_inputs_fields = confirmation_code_inputs.find_elements(by=By.TAG_NAME, value="input")

            code = mail_getting(account["mail"], account["password"])
            for _ in range(20):
                print(code)
                if code is None:
                    time.sleep(5)
                    try:
                        code = mail_getting(account["mail"], account["password"])
                    except:
                        continue
                else:
                    break

            if code is not None:

                for index, element in enumerate(confirmation_code_inputs_fields):
                    element.send_keys(code[index])
                    time.sleep(0.6)

                continue_btn = driver_waiting.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-otp-update-form"]/div[3]/div/input')))
                time.sleep(1)

                try:

                    continue_btn.click()

                except:
                    driver.execute_script("arguments[0].click();", continue_btn)

                update_on_uefa_status(account["mail"])

                time.sleep(3)

                if account["country"] != "":
                    choose_country_btn = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="gigya-profile-form"]/div[1]/div[2]/div/div/div/input')))
                    choose_country_btn.click()
                    time.sleep(0.3)
                    choose_country_btn.send_keys(account["country"])
                    time.sleep(1)
                    select_country_li = \
                        driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "searchable-select-list-dropdown-item")))
                    select_country_li.click()

                time.sleep(0.5)

                if account["champ_club"] != "":
                    choose_champ_club_btn = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="gigya-profile-form"]/div[1]/div[3]/div/div[1]/div/div[2]')))
                    choose_champ_club_btn.click()
                    time.sleep(0.3)
                    choose_champ_club_inp = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="gigya-profile-form"]/div[1]'
                                                    '/div[3]/div/div[1]/div/div/div[1]/input')))
                    choose_champ_club_inp.send_keys(account["champ_club"])
                    time.sleep(1)
                    select_club = \
                        driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "idp-sayt-grid__dropdown--item")))
                    select_club.click()
                time.sleep(0.5)

                if account["europe_club"] != "":
                    choose_europe_club_btn = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="gigya-profile-form"]/div[1]'
                                                    '/div[3]/div/div[2]/div/div[2]')))
                    choose_europe_club_btn.click()
                    time.sleep(0.3)
                    choose_europe_club_inp = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                              '/div[1]/div[3]/div/div[2]/div/div/div[1]/input')))
                    choose_europe_club_inp.send_keys(account["europe_club"])
                    time.sleep(1)
                    select_club = \
                        driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "idp-sayt-grid__dropdown--item")))
                    select_club.click()
                time.sleep(0.5)

                if account["male_club"] != "":
                    choose_male_club_btn = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                              '/div[1]/div[3]/div/div[3]/div[2]/div')))
                    choose_male_club_btn.click()
                    time.sleep(0.3)
                    choose_male_club_inp = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                              '/div[1]/div[3]/div/div[3]/div[2]/div/div[1]/input')))
                    choose_male_club_inp.send_keys(account["male_club"])
                    time.sleep(1)
                    select_club = \
                        driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "idp-sayt__dropdown--item")))
                    select_club.click()

                time.sleep(0.5)

                if account["female_club"] != "":
                    choose_female_club_btn = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                              '/div[1]/div[3]/div/div[4]/div[2]/div')))
                    choose_female_club_btn.click()
                    time.sleep(0.3)
                    choose_female_club_inp = driver_waiting.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                              '/div[1]/div[3]/div/div[4]/div[2]/div/div[1]/input')))
                    choose_female_club_inp.send_keys(account["female_club"])
                    time.sleep(1)
                    select_club = \
                        driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "idp-sayt__dropdown--item")))
                    select_club.click()

                time.sleep(0.5)

                save_btn = driver_waiting.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-profile-form"]'
                                                                                      '/div[2]/div[1]/input')))
                save_btn.click()

                time.sleep(3)

            else:
                raise CodeUndefinedException

        except Exception as ex:
            driver.save_screenshot(f'{datetime.datetime.now()}.png')
            print(ex)

        try:
            driver.close()
            driver.quit()
            print("Registration is done")
        except Exception as ex:
            print(ex)
            raise DriverUndefinedException









