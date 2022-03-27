import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from creds import USERNAME, PASSWORD
from cssselectors import USERNAME_INPUT_FIELD, PASSWORD_INPUT_FIELD, LOGIN_BTN


def login2(browser):
    browser.find_element_by_id("txtNRIC").send_keys(USERNAME)
    browser.find_element_by_id("txtPassword").send_keys(PASSWORD)
    browser.find_element_by_id("txtPassword").send_keys(Keys.ENTER)


def login(browser):
    # WebDriverWait(browser, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, USERNAME_INPUT_FIELD))
    # ).send_keys(USERNAME)
    # WebDriverWait(browser, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, PASSWORD_INPUT_FIELD))
    # ).send_keys(PASSWORD)
    # WebDriverWait(browser, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BTN))
    # ).send_keys(Keys.ENTER)
    browser.find_element_by_css_selector(USERNAME_INPUT_FIELD).send_keys(USERNAME)
    browser.find_element_by_css_selector(PASSWORD_INPUT_FIELD).send_keys(PASSWORD)
    browser.find_element_by_css_selector(LOGIN_BTN).click()


def wait_for_element(browser, selector):
    WebDriverWait(browser, timeout=3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def get_slot_details(attr_value_str):
    # doTooltipV(event,0, "07/06/2021 (Mon)","7","19:20","21:00","BBDC"); SetMouseOverToggleColor("cell2_6")
    details = {}
    chunks = re.findall('"([^"]*)"', attr_value_str)
    details["session_num"] = chunks[1]
    details["session_timing"] = "{} - {}".format(chunks[2], chunks[3])
    return details


#  unused
def is_blacklisted(date):
    return False


def is_after_current_booking(date, current_booking_date):
    current = current_booking_date.split("/")
    against = date.split("/")
    if int(current[1]) < int(against[1]):
        return True
    elif int(current[0]) < int(against[0]):
        return True
    return False
