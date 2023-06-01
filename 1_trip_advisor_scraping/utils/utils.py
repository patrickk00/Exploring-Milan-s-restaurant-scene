import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)


def get_reviews(index, button, driver):

    print("3")
    main_window_handle = driver.current_window_handle
    print("3.5")
    #WebDriverWait(driver, 30,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located(button))

    actions = ActionChains(driver)
    actions.move_to_element(button).perform()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(button)).click()

    for handle in driver.window_handles:
        if handle != main_window_handle:
            driver.switch_to.window(handle)
            break
    #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))).click()

    reviews = []
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="rev_wrap ui_columns is-multiline"]')))

    rev = driver.find_elements(By.XPATH, '//div[@class="rev_wrap ui_columns is-multiline"]')
    for r in rev:
        bubbles = r.find_element(By.CLASS_NAME, 'ui_bubble_rating').get_attribute('class')
        title = r.find_element(By.TAG_NAME, 'a').text
        description = r.find_element(By.CLASS_NAME, 'partial_entry').text
        reviews.append({'id_restaurants': index, 'bubbles' : bubbles.split(' ')[1], 'title': title, 'description': description})

    driver.close()
    driver.switch_to.window(main_window_handle)
    return reviews


def save_in_csv(restaurants, reviews):
    df = pd.DataFrame(restaurants)
    df.to_csv('./output_files/restaurants.csv', index=False)
    df = pd.DataFrame(reviews)
    df.to_csv('./output_files/reviews.csv', index=False)