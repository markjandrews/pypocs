import sys

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(argv=sys.argv[1:]):
    driver = webdriver.Firefox()
    # driver.get("http://www.python.org")
    # assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

    # driver.get("http://www.nswlotteries.com/")
    driver.get('https://tatts.com/nswlotteries/buy-lotto/purchase-ticket?product=O')
    user_element = driver.find_element_by_id("Username")
    user_element.send_keys('markj.andrews@gmail.com')
    password_element = driver.find_element_by_id("Password")
    password_element.send_keys('daria2Hug')
    login_element = driver.find_element_by_id("Login")
    login_element.click()

    fifty_games_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@gamecount="50"]')))

    fifty_games_element.click()
    games_table_element = driver.find_element_by_id('GameSelectionsTbl')
    for games_row in games_table_element.find_elements_by_xpath('//tr'):
        games_row.click()
        print(games_row)
        time.sleep(1.5)
    # logout_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnLogout')))
    # logout_element.click()

    # driver.close()


if __name__ == '__main__':
    main()
