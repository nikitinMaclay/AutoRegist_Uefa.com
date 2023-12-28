import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    # options.add_argument(r"--user-data-dir=")  # change to your profile
    # options.add_argument('profile-directory=Default')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    # profile_directory = r'%AppData%\Mozilla\Firefox\Profiles\z6l67q5o.uefa'
    # profile = webdriver.FirefoxProfile(os.path.expandvars(profile_directory))
    # options.profile = profile

    driver = webdriver.Chrome(options=options)

    return driver

