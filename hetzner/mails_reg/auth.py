import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Authorization function
def auth(driver, hetzner_acc, hetzner_password):
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@class="login-image-container"]')))
    # input username service
    driver.find_element(by=By.XPATH, value='//input[@name="_username"]').send_keys(f'{hetzner_acc}')
    # input password service
    driver.find_element(by=By.XPATH, value='//input[@name="_password"]').send_keys(f'{hetzner_password}')
    driver.find_element(by=By.XPATH, value='//input[@type="submit"]').click()
    time.sleep(2)
