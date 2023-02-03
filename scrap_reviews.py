import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import random

import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

lock = threading.Lock()

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'
]
# df = pd.read_csv("file.csv")
# for index, row in df.iterrows():
#     print(row)

restaurants_df = pd.read_csv('./output/trip_restaurants_final.csv')
reviews_df = pd.read_csv('./output/trip_reviews_link.csv')
backup_df = pd.read_csv('./output/reviews_save.csv')
ua = UserAgent()
def scrape_reviews(url, id, driver):
    #user_agent = ua.random
    reviews = []
    options = webdriver.ChromeOptions()
    # options.add_argument('user-agent={}'.format(user_agent))
    #options.add_argument(f'user-agent={random.choice(user_agents)}')


    #with lock:
        # actions = ActionChains(driver)
        # actions.key_down(Keys.COMMAND).send_keys('t').key_up(Keys.COMMAND).perform()
    #driver.execute_script("window.open('about:blank', '_blank');")
    #driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    #time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("soup: ",soup)
    #driver.quit()
    elements = soup.find_all('div', class_='review-container')
    #print(elements)
    #restaurant_name = soup.find('h1', class_='HjBfq').text
    print("address: ", soup.find('a', href= '#MAPVIEW', class_='AYHFM'))
    address = ''
    if soup.find('a', href= '#MAPVIEW', class_='AYHFM'):
        address = soup.find('a', href= '#MAPVIEW', class_='AYHFM').text
    #print(restaurant_name)
    print("ID: ---->", id)
    print(address)
    rev =[]
    for element in elements:
        bubbles =element.find('span', class_='ui_bubble_rating')
        bubbles = bubbles['class'][1]
        title = element.find('a', class_='title').text
        description = element.find('p', class_='partial_entry').text
        rev.append({'bubbles' : bubbles, 'title': title, 'description': description})
    reviews.append({'id': id, 'address_trip': address, 'reviews': rev})
    return reviews

results =[]
count = 0
driver = webdriver.Chrome()
time.sleep(1)
for url in reviews_df.iloc[2020:].iterrows():
    time.sleep(1)

    results.extend(scrape_reviews(url[1]['link'], url[1]['id'], driver))
    if count >= 100:
        count = 0
        df = pd.DataFrame(results)
        backup_df = pd.concat([backup_df, df])
        results = []
        backup_df.to_csv(f'./output/reviews_save.csv', index=False)   
    else:
        count +=1    
driver.quit()

# non usiamo i thread perchè trip advisor blocca!!!!!!!!!!!
# with ThreadPoolExecutor(max_workers=1) as executor:
#     futures = [executor.submit(scrape_reviews, url[1]['link'], url[1]['id']) for url in reviews_df.iloc[403:].iterrows()]
#     results = []
#     count = 0
#     df_save = pd.DataFrame()
#     for future in as_completed(futures):
#         results.extend(future.result())
#         count +=1
#         if count > 100:
#              df = pd.DataFrame(results)
#              df = pd.concat([backup_df, df])
#              df.to_csv('./output/reviews_save.csv', index=False)
#              count = 0
#     df = pd.DataFrame(results)
#     df = restaurants_df.merge(df, how='left', on='id')

#     df.to_csv('./output/restaurants_reviews_definitive.csv', index=False)