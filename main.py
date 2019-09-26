import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import pyautogui

import numpy as np
import cv2

LOGIN = "347123456"
PASSWORD = "password"
SCROLL_TO_PX = 30000

AVERAGE_POST_SIZE_PX = 750

driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
driver.get("https://www.instagram.com/accounts/login/")
driver.set_window_position(0, 0)
driver.set_window_size(width=400, height=800)


def login(login, password):
    # first elem
    elem = driver.find_element_by_name("username")
    elem.clear()
    elem.send_keys(login)
    # second elem
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(password)
    # submit
    elem.send_keys(Keys.RETURN)


def turn_off_popup_if_exists():
    try:
        elem = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_tag_name('h2'))

    finally:
        dom = BeautifulSoup(driver.page_source, 'html.parser')
        elems = dom.find_all('h2')
        for elem in elems:
            if elem.get_text() == "Turn on Notifications":
                print('Notification Window Found')
                elem = driver.find_element_by_css_selector('div[role=dialog] button:last-of-type')
                elem.click()
                time.sleep(1)
                driver.refresh()


def parse_coordinates(screenshot, screenshot_debug, image_pattern = "pattern.png"):
    img_rgb = cv2.imread(screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_pattern, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    result = []
    for pt in zip(*loc[::-1]):
        # skip image in the header
        if pt[0] > 100:
            continue
        result.append(pt)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv2.imwrite(screenshot_debug, img_rgb)

    return result


def run(width=100):
    time.sleep(1)

    driver.execute_script("window.scrollTo(0," + str(width) + ")")
    driver.save_screenshot("data/screenshot" + str(width) + ".png")

    pag_coordinates = pyautogui.locateOnScreen("pattern.png")
    print("PAG parsed coords", pag_coordinates)

    coords = parse_coordinates("data/screenshot" + str(width) + ".png", "data/screenshot" + str(width) + "_debug.png")
    for c in coords:
        print("CV2 parsed coords", c)
        X_OFFSET = 25
        Y_OFFSET = 100
        pyautogui.click(x=c[0] + X_OFFSET, y=c[1] + Y_OFFSET)


print("Logging in...")
time.sleep(1)
login(LOGIN, PASSWORD)

print('Waiting for the next page...')
time.sleep(2)
print('Loaded Page', driver.title)

turn_off_popup_if_exists()

run()

for y in range(100, SCROLL_TO_PX, AVERAGE_POST_SIZE_PX):
    run(width=y)

driver.close()
print("Finished.")