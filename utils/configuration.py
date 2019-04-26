import argparse
from selenium import webdriver
import os


def login(driver, usr, psw):
    driver.get("https://idp.polito.it/idp/x509mixed-login")
    user = driver.find_element_by_name('j_username')
    user.send_keys(usr)
    password = driver.find_element_by_name("j_password")
    password.send_keys(psw)
    btn = driver.find_element_by_id('usernamepassword')
    btn.submit()


def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless') #It works only with video_lectures download
    options.add_argument('window-size=1200x600')
    prefs = {'download.default_directory': os.getenv('HOME') + '/Downloads'}
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(executable_path='bin/chromedriver', options=options)


def arg_parser():
    parser = argparse.ArgumentParser(description='PoliTo Videolectures downloader')
    parser.add_argument('-user', '-u', help='Username', nargs='?', type=str)
    parser.add_argument('-psw', '-p', help='password', nargs='?', type=str)
    return parser.parse_args()

