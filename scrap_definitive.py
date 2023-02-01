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
from utils.utils import get_reviews, save_in_csv

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

def save_in_csv(restaurantsList, reviewLinks):
    df = pd.DataFrame(restaurantsList)
    df.to_csv('./output_files/restaurants_definitive.csv', index=False)
    df = pd.DataFrame(reviewLinks)
    df.to_csv('./output_files/reviewLinks.csv', index=False)

def get_restaurant_data(e, count):
    title = e.find_element(By.TAG_NAME, 'a')
    link = title.get_attribute('href')
    reviewLinks.append({'id': count, 'link':link})
    #reviewList.extend(get_reviews(index = count, button = title, driver=driver))

    try:
        reviews = e.find_element(By.CLASS_NAME, 'LBKCf')
        reviews_number = e.find_element(By.CLASS_NAME, 'IiChw')
        reviews_bubble = reviews.find_element(By.TAG_NAME, 'svg')
        r_b = reviews_bubble.get_attribute('aria-label')

        type = e.find_element(By.CLASS_NAME, 'bAdrM')
        type_elems = type.find_elements(By.CLASS_NAME, "qAvoV")

        if(len(type_elems)<1):
            cook_type = '?'
        else:
            cook_type = type_elems[0].text
        if(len(type_elems)<2):
            expensive = '?'
        else:
            expensive = type_elems[1].text
        title = title.text 
        r_bubbles=r_b
        r_number=reviews_number.text
        cook_type=cook_type
        expensive=expensive
    except Exception as e:
        print("EXCEPTION 3: ", e)
        r_bubbles = '?'
        r_number = 0
        cook_type = '?'
        expensive = '?'
        pass
    restaurant = {'id': count, 'title': title, 'r_bubbles': r_bubbles, 'r_number': r_number, 'cook_type': cook_type, 'expensive': expensive}
    print('////////////////////////')
    print(restaurant)
    return restaurant

driver = webdriver.Chrome()

driver.get("https://www.tripadvisor.it/Restaurants-g187849-Milan_Lombardy.html")
driver.maximize_window()

restaurantsList = []
reviewLinks = []

  
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))).click()
time.sleep(5)
count = 0
while True:
    try:
        time.sleep(2)
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "YtrWs")))
        elem = driver.find_element(By.CLASS_NAME, "YtrWs")
        elements = elem.find_elements(By.XPATH, "//div[@class='zdCeB Vt o']")
        for e in elements:
            print("element!!!!!!!!", count)
            #try:
            if e.text.find('Sponsorizzato') == -1:

                restaurantsList.append(get_restaurant_data(e, count))
                count += 1
            print("end element!!!!!!!!")

            # except Exception as e:
            #         print("EXCEPTION", e)
            #         count += 1
            #         save_in_csv(restaurantsList, reviewLinks)               
            #         pass
        print("before click!!!!!!!!")

        if len(driver.find_elements(By.XPATH, '//span[@class="nav next disabled"]')) != 0:
            break
        time.sleep(2)
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]')))
        element = driver.find_element(By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]')

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]'))).click()
        print("after click!!!!!!!!")

    except Exception as e:
        print("EXCEPTION 2", e)
        save_in_csv(restaurantsList, reviewLinks)               
        element = driver.find_element(By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]')
        link=element.get_attribute("href")
        driver.get(link)
        pass


        #driver.find_element(By.XPATH, './/a[@class="nav next rndBtn ui_button primary taLnk"]').click()

save_in_csv(restaurantsList, reviewLinks)


#elem.clear()
driver.close()




