import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.common.exceptions import NoSuchElementException

from uefa.uefa_site_reg.code_receiving import mail_getting
from hetzner.databases_manage.database_scripts import update_on_uefa_status

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


class AutoRegistrator:
    def __init__(self, email, password, first_name, last_name,
                 birth_day, birth_month, birth_year, password_for_mail, link="https://www.uefa.com/"):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
        self.link = link
        self.password_for_mail = password_for_mail
        self.driver: webdriver.firefox = None
        self.driver_waiting = None

    def driver_initialisation(self):
        options = Options()
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = webdriver.Firefox(options=options)
        self.driver_waiting: WebDriverWait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def start_registration(self):
        options = Options()
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = webdriver.Firefox(options=options)
        self.driver_waiting: WebDriverWait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

        if self.driver is None:
            raise DriverUndefinedException()

        self.driver.get(self.link)
        accept_cookies_btn = \
            self.driver_waiting.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies_btn.click()
        login_btn = self.driver_waiting.until(EC.element_to_be_clickable((By.CLASS_NAME, "nav-login__button")))
        login_btn.click()

        new_account_btn = self.driver_waiting.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="gigya-login-form"]/div[4]/a')))
        new_account_btn.click()

        time.sleep(1.5)
        email_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-75074230944436030"]')))
        password_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-password-59919533498235100"]')))
        first_name_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-130722358975432270"]')))
        last_name_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-30497114450394400"]')))
        email_field.send_keys(self.email)
        time.sleep(0.7)
        password_field.send_keys(self.password)
        time.sleep(0.7)
        first_name_field.send_keys(self.first_name)
        time.sleep(0.7)
        last_name_field.send_keys(self.last_name)
        time.sleep(0.7)

        birth_day_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-88315185881230510"]')))
        birth_month_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-105406014904922500"]')))
        birth_year_field = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-textbox-32538633360993784"]')))

        birth_day_field.send_keys(self.birth_day)
        time.sleep(0.7)
        birth_month_field.send_keys(self.birth_month)
        time.sleep(0.7)
        birth_year_field.send_keys(self.birth_year)
        time.sleep(0.7)

        accept_terms_and_conditions_checkbox = self.driver_waiting.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gigya-register-form"]/div[1]/div[11]/label/span')))

        self.driver.execute_script("arguments[0].click();", accept_terms_and_conditions_checkbox)

        create_account_btn = self.driver_waiting.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="gigya-register-form"]/div[1]/div[13]/input')))

        create_account_btn.click()

        time.sleep(1)
        self.driver.switch_to.default_content()

        captcha_iframe = self.driver_waiting.until(EC.visibility_of_element_located((
            By.XPATH, '/html/body/div[12]/div[2]/iframe')))

        captcha_url = captcha_iframe.get_attribute("src")
        captcha_sitekey = captcha_url.split("k=")[-1]
        result = solver.solve_captcha(captcha_sitekey, self.link)
        print(result)
        self.driver.execute_script(f"window.___grecaptcha_cfg.clients[0].A.A.callback('{result}')")
        time.sleep(5)
        actions = ActionChains(self.driver)
        actions.move_by_offset(100, 100).perform()
        actions.click().perform()
        time.sleep(3)
        try:
            confirmation_code_inputs = self.driver_waiting.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "idp-otp-login-pin")))

            confirmation_code_inputs_fields = confirmation_code_inputs.find_elements(by=By.TAG_NAME, value="input")

            code = mail_getting(self.email, self.password_for_mail)
            for _ in range(4):
                print(code)
                if code is None:
                    time.sleep(15)
                    code = mail_getting(self.email, self.password_for_mail)
                else:
                    break

            if code is not None:

                for index, element in enumerate(confirmation_code_inputs_fields):
                    element.send_keys(code[index])
                    time.sleep(0.6)

                continue_btn = self.driver_waiting.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="gigya-otp-update-form"]/div[3]/div/input')))
                time.sleep(1)

                continue_btn.click()

                update_on_uefa_status(self.email)

                time.sleep(10)

            else:
                raise CodeUndefinedException

        except NoSuchElementException as ex:
            print(ex)

        try:
            self.driver.quit()
        except Exception as ex:
            print(ex)
            raise DriverUndefinedException

    def start_login(self):
        pass

    def close_session(self):
        try:
            self.driver.quit()
        except Exception as ex:
            print(ex)
            raise DriverUndefinedException
