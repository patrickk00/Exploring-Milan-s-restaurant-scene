import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

lock = threading.Lock()


# df = pd.read_csv("file.csv")
# for index, row in df.iterrows():
#     print(row)
driver = webdriver.Chrome()

reviews_df = pd.read_csv('./output_files/reviewLinks.csv')

def scrape_reviews(url, driver, id):
    reviews = []

    with lock:
        # actions = ActionChains(driver)
        # actions.key_down(Keys.COMMAND).send_keys('t').key_up(Keys.COMMAND).perform()
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    #time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #driver.quit()
    elements = soup.find_all('div', class_='review-container')
    #print(elements)
    # Extract the text from each element
    restaurant_name = soup.find('h1', class_='HjBfq').text
    address = soup.find('a', href= '#MAPVIEW', class_='AYHFM').text
    print(restaurant_name)
    rev =[]
    for element in elements:
        bubbles =element.find('span', class_='ui_bubble_rating')
        bubbles = bubbles['class'][1]
        title = element.find('a', class_='title').text
        description = element.find('p', class_='partial_entry').text
        rev.append({'bubbles' : bubbles, 'title': title, 'description': description})
    reviews.append({'id': id, 'restaurant': restaurant_name, 'address_trip': address, 'reviews': rev})
    return reviews



with ThreadPoolExecutor() as executor:
    futures = [executor.submit(scrape_reviews, url[1]['link'], driver, url[1]['id']) for url in reviews_df.iterrows()]
    results = []
    for future in as_completed(futures):
        results.extend(future.result())

    df = pd.DataFrame(results)
    df.to_csv('./output_files/reviews.csv', index=False)