import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CANDIDATE_JSON_PATH = r'C:\Users\Mark\PycharmProjects\NumbersUpOZ\ozcandidate.json'


def add_draw(table_element, values):
    for value in values:
        click_ball(table_element, value)


def click_ball(table_element, value):

    ball_element = table_element.find_element_by_xpath('//td[@selection="%s"]' % value)
    if 'rgb(255, 255, 255)' not in ball_element.get_attribute("style"):
        return

    ball_element.click()


def main(argv=sys.argv[1:]):

    with open(CANDIDATE_JSON_PATH, 'r') as inf:
        candidates = sorted(json.load(inf))

    driver = webdriver.Firefox()
    driver.get('https://tatts.com/nswlotteries/buy-lotto/purchase-ticket?product=OzLotto')
    user_element = driver.find_element_by_id("Username")
    user_element.send_keys('markj.andrews@gmail.com')
    password_element = driver.find_element_by_id("Password")
    password_element.send_keys('daria2Hug')
    login_element = driver.find_element_by_id("Login")
    login_element.click()

    fifty_games_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@gamecount="50"]')))
    fifty_games_element.click()

    for ticket_number in range(2):

        ball_table_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'GridSelectionsTbl')))

        for ticket_row_number in range(1, 51):
            draw_number = (ticket_number * 50) + ticket_row_number
            candidate = candidates[draw_number-1]
            games_row_element = driver.find_element_by_xpath(
                    '//div[@class="gameNumberDiv"]/span[contains(text(), "%s")]' % ticket_row_number)
            games_row_element.click()
            add_draw(ball_table_element, candidate)

        add_to_cart_element = driver.find_element_by_id('AddToTrolleyBtn')
        add_to_cart_element.click()
        time.sleep(5)

        driver.get('https://tatts.com/nswlotteries/buy-lotto/purchase-ticket?product=OzLotto')
        fifty_games_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@gamecount="50"]')))
        fifty_games_element.click()

    # logout_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnLogout')))
    # logout_element.click()

    # driver.close()


if __name__ == '__main__':
    main()
