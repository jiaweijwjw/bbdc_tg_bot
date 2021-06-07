import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tg import TelegramChatbot
from constants import LOGIN_URL, LOGIN_TITLE
from helpers import (
    login,
    wait_for_element,
    get_slot_details,
    is_blacklisted,
    is_after_current_booking,
)
from cssselectors import (
    CLASS_2A_RADIO_BTN,
    SELECT_COURSE_BTN,
    SELECT_COURSE_FORM,
    SIDE_BAR_BOOKING_STATEMENT,
    BOOKING_STATEMENT_FORM,
    MAIN_FRAME,
    SIDE_FRAME,
    CURRENT_PRACTICAL_TRAINING_BOOKING,
    SIDE_BAR_PRACTICAL_TRAINING_BOOKING,
    PRACTICAL_TRAINING_BOOKING_FORM,
    PRACTICAL_TRAINING_BOOKING_OPTIONS_COMMON_PARENT,
    ALL_MONTHS,
    ALL_SESSIONS,
    ALL_DAYS,
    SEARCH_PRACTICAL_TRAINING_SLOTS_BTN,
    AVAILABLE_PRACTICAL_TRAINING_SLOTS_FORM,
    PRACTICAL_TRAINING_SLOTS_TABLE,
)

bot = TelegramChatbot()
msg = "BBDC: \n\n"
current_booking = {}

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-dev-shm-usage")
# options.add_argument("window-size=1920x1080")
options.add_argument("--disable-gpu")
browser = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(), options=options
)
# browser = webdriver.Chrome(
#     executable_path=os.environ.get("PATH_TO_CHROMEDRIVER"), options=options
# )


try:
    # browser.get("https://www.instagram.com/accounts/login/")
    # print(browser.current_url)
    # print(browser.title)
    # WebDriverWait(browser, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
    # ).send_keys("mychillnook")
    # print(browser.title)

    browser.get(LOGIN_URL)  # .get() by default already waits for page to load.
    # wait_for_element(browser, "form[action='header2.asp']")
    print(browser.current_url)
    print(LOGIN_URL)
    print(browser.title)
    print(LOGIN_TITLE)
    if browser.current_url == LOGIN_URL and browser.title == LOGIN_TITLE:
        print(browser.title)
        try:
            login(browser)
            browser.switch_to.alert.dismiss()
            browser.switch_to.default_content()
        except Exception as e:
            print(e)

        # login(browser)
        # wait_for_element(browser, "body.insecure-form")
        # WebDriverWait(browser, timeout=3).until(
        #     EC.presence_of_element_located((By.ID, "proceed-button"))
        # )
        # browser.find_element_by_id("proceed-button").click()
        wait_for_element(browser, SELECT_COURSE_FORM)
        print(browser.title)
        class2A_radio_btn = browser.find_element_by_css_selector(CLASS_2A_RADIO_BTN)
        is_class2A = class2A_radio_btn.is_selected()
        if not is_class2A:
            class2A_radio_btn.click()
        browser.find_element_by_css_selector(SELECT_COURSE_BTN).click()
        wait_for_element(browser, SIDE_FRAME)
        browser.switch_to.frame(browser.find_element_by_css_selector(SIDE_FRAME))

        # For checking if there is any slot >48 hours earlier than my current slot
        browser.find_element_by_css_selector(SIDE_BAR_BOOKING_STATEMENT).click()
        browser.switch_to.default_content()
        wait_for_element(browser, MAIN_FRAME)
        browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
        wait_for_element(browser, BOOKING_STATEMENT_FORM)
        page = browser.find_element_by_css_selector("p.pgtitle")
        if page.text == "Booking Statement":
            current_practical_training_booking = (
                page.parent.find_elements_by_css_selector(
                    CURRENT_PRACTICAL_TRAINING_BOOKING
                )
            )
            booking_details = "Current practical booking: \n"
            date = current_practical_training_booking[0].text
            session = current_practical_training_booking[1].text  # Unused for now
            time = current_practical_training_booking[2].text
            current_booking = {"date": date, "session": session, "time": time}
            booking_details += "Date: {} \nTime: {}\n\n".format(date, time)
            msg += booking_details
        browser.switch_to.default_content()
        wait_for_element(browser, SIDE_FRAME)
        browser.switch_to.frame(browser.find_element_by_css_selector(SIDE_FRAME))

        browser.find_element_by_css_selector(
            SIDE_BAR_PRACTICAL_TRAINING_BOOKING
        ).click()
        browser.switch_to.default_content()
        wait_for_element(browser, MAIN_FRAME)
        browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
        wait_for_element(browser, PRACTICAL_TRAINING_BOOKING_FORM)
        # check all months, sessions and days
        common_parent = browser.find_elements_by_css_selector(
            PRACTICAL_TRAINING_BOOKING_OPTIONS_COMMON_PARENT
        )
        common_parent[0].find_element_by_css_selector(ALL_MONTHS).click()
        common_parent[2].find_element_by_css_selector(ALL_SESSIONS).click()
        common_parent[5].find_element_by_css_selector(ALL_DAYS).click()
        browser.find_element_by_css_selector(
            SEARCH_PRACTICAL_TRAINING_SLOTS_BTN
        ).click()
        alert = browser.switch_to.alert.dismiss()
        browser.switch_to.default_content()
        wait_for_element(browser, MAIN_FRAME)
        browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
        wait_for_element(browser, AVAILABLE_PRACTICAL_TRAINING_SLOTS_FORM)
        table = browser.find_element_by_css_selector(PRACTICAL_TRAINING_SLOTS_TABLE)
        soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        table_rows = soup.find_all("tr", bgcolor="#FFFFFF", recursive=False)

        practical_training_schedule = "Available practical training slots: \n"
        for row in table_rows:
            daydate = row.find("td")
            date = daydate.contents[0].string  # contents[1] is the <br> line break tag
            if is_blacklisted(date):
                continue
            elif is_after_current_booking(date, current_booking["date"]):
                break
            day = daydate.contents[2].string
            available_slots = row.find_all("td", recursive=False)
            sessions = ""
            # count = 0
            for slot in available_slots:
                if slot.has_attr("onmouseover"):
                    # count += 1
                    attr_value_str = slot.get("onmouseover")
                    session_details = get_slot_details(
                        attr_value_str
                    )  # session_details["session_num"] is unused for now
                    sessions += "   ({}). Time: {}\n".format(
                        session_details["session_num"],
                        session_details["session_timing"],
                    )
            practical_training_schedule += "Date: {}, {} \nSessions: \n{}\n".format(
                date, day, sessions
            )
        msg += practical_training_schedule
        # print(msg)
        with open("msg.txt", "r+") as f:
            data = f.read()
            if msg != data:
                f.write(msg)
                bot.send_practical_training_slots(msg)
        print("end")
        bot.send_practical_training_slots("hi")
except Exception as e:
    print(e)
finally:
    browser.quit()


# with webdriver.Chrome(ChromeDriverManager().install(), options=options) as browser:
#     browser.get(LOGIN_URL)  # .get() by default already waits for page to load.
#     # browser.get(
#     #     "https://stackoverflow.com/questions/67787707/how-can-i-make-my-python-selenium-project-work-on-heroku"
#     # )
#     print(browser.title)
#     print(browser.current_url)
#     if browser.current_url == LOGIN_URL and browser.title == LOGIN_TITLE:
#         print(browser.title)
#         login(browser)
#         wait_for_element(browser, SELECT_COURSE_FORM)
#         print(browser.title)
#         class2A_radio_btn = browser.find_element_by_css_selector(CLASS_2A_RADIO_BTN)
#         is_class2A = class2A_radio_btn.is_selected()
#         if not is_class2A:
#             class2A_radio_btn.click()
#         browser.find_element_by_css_selector(SELECT_COURSE_BTN).click()
#         wait_for_element(browser, SIDE_FRAME)
#         browser.switch_to.frame(browser.find_element_by_css_selector(SIDE_FRAME))

#         # For checking if there is any slot >48 hours earlier than my current slot
#         browser.find_element_by_css_selector(SIDE_BAR_BOOKING_STATEMENT).click()
#         browser.switch_to.default_content()
#         wait_for_element(browser, MAIN_FRAME)
#         browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
#         wait_for_element(browser, BOOKING_STATEMENT_FORM)
#         page = browser.find_element_by_css_selector("p.pgtitle")
#         if page.text == "Booking Statement":
#             current_practical_training_booking = (
#                 page.parent.find_elements_by_css_selector(
#                     CURRENT_PRACTICAL_TRAINING_BOOKING
#                 )
#             )
#             booking_details = "Current practical booking: \n"
#             date = current_practical_training_booking[0].text
#             session = current_practical_training_booking[1].text  # Unused for now
#             time = current_practical_training_booking[2].text
#             current_booking = {"date": date, "session": session, "time": time}
#             booking_details += "Date: {} \nTime: {}\n\n".format(date, time)
#             msg += booking_details
#         browser.switch_to.default_content()
#         wait_for_element(browser, SIDE_FRAME)
#         browser.switch_to.frame(browser.find_element_by_css_selector(SIDE_FRAME))

#         browser.find_element_by_css_selector(
#             SIDE_BAR_PRACTICAL_TRAINING_BOOKING
#         ).click()
#         browser.switch_to.default_content()
#         wait_for_element(browser, MAIN_FRAME)
#         browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
#         wait_for_element(browser, PRACTICAL_TRAINING_BOOKING_FORM)
#         # check all months, sessions and days
#         common_parent = browser.find_elements_by_css_selector(
#             PRACTICAL_TRAINING_BOOKING_OPTIONS_COMMON_PARENT
#         )
#         common_parent[0].find_element_by_css_selector(ALL_MONTHS).click()
#         common_parent[2].find_element_by_css_selector(ALL_SESSIONS).click()
#         common_parent[5].find_element_by_css_selector(ALL_DAYS).click()
#         browser.find_element_by_css_selector(
#             SEARCH_PRACTICAL_TRAINING_SLOTS_BTN
#         ).click()
#         alert = browser.switch_to.alert.dismiss()
#         browser.switch_to.default_content()
#         wait_for_element(browser, MAIN_FRAME)
#         browser.switch_to.frame(browser.find_element_by_css_selector(MAIN_FRAME))
#         wait_for_element(browser, AVAILABLE_PRACTICAL_TRAINING_SLOTS_FORM)
#         table = browser.find_element_by_css_selector(PRACTICAL_TRAINING_SLOTS_TABLE)
#         soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
#         table_rows = soup.find_all("tr", bgcolor="#FFFFFF", recursive=False)

#         practical_training_schedule = "Available practical training slots: \n"
#         for row in table_rows:
#             daydate = row.find("td")
#             date = daydate.contents[0].string  # contents[1] is the <br> line break tag
#             if is_blacklisted(date):
#                 continue
#             elif is_after_current_booking(date, current_booking["date"]):
#                 break
#             day = daydate.contents[2].string
#             available_slots = row.find_all("td", recursive=False)
#             sessions = ""
#             # count = 0
#             for slot in available_slots:
#                 if slot.has_attr("onmouseover"):
#                     # count += 1
#                     attr_value_str = slot.get("onmouseover")
#                     session_details = get_slot_details(
#                         attr_value_str
#                     )  # session_details["session_num"] is unused for now
#                     sessions += "   ({}). Time: {}\n".format(
#                         session_details["session_num"],
#                         session_details["session_timing"],
#                     )
#             practical_training_schedule += "Date: {}, {} \nSessions: \n{}\n".format(
#                 date, day, sessions
#             )
#         msg += practical_training_schedule
#         # print(msg)
#         with open("msg.txt", "r+") as f:
#             data = f.read()
#             if msg != data:
#                 f.write(msg)
#                 bot.send_practical_training_slots(msg)
#         print("end")
#         bot.send_practical_training_slots("fuck")
#         browser.quit()
