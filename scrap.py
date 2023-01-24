import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
#AIzaSyDPahJWr0nYbAJnGc0bmV1BRQ96eQ6PqhM GOOGLE API KEY

class Restaurant:
    def _init_(self, title, r_bubbles, r_number, cook_type, expensive):
        self.title = title
        self.r_bubbles = r_bubbles
        self.r_number = r_number
        self.cook_type = cook_type
        self.expensive = expensive
    def as_dict(self):
        return {'title': self.title, 'r_bubbles': self.r_bubbles, 'r_number': self.r_number, 'cook_type': self.cook_type, 'expensive': self.expensive}


driver = webdriver.Chrome()

driver.get("https://www.tripadvisor.it/Restaurants-g187849-Milan_Lombardy.html")
driver.maximize_window()

restaurantsList = []
print("helloooo")
time.sleep(5)

  
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))).click()


while len(driver.find_elements(By.XPATH, '//span[@class="nav next disabled"]')) == 0:

    time.sleep(2)
    elem = driver.find_element(By.CLASS_NAME, "YtrWs")
    elements = elem.find_elements(By.XPATH, "//div[@class='zdCeB Vt o']")

    for e in elements:
        print(e.text)
        title = e.find_element(By.TAG_NAME, 'a')
        reviews = e.find_element(By.CLASS_NAME, 'LBKCf')
        reviews_number = e.find_element(By.CLASS_NAME, 'IiChw')
        reviews_bubble = reviews.find_element(By.TAG_NAME, 'svg')
        r_b = reviews_bubble.get_attribute('aria-label')
        #print(r_b)
        #print(reviews_number.text)
        type = e.find_element(By.CLASS_NAME, 'bAdrM')
        type_elems = type.find_elements(By.CLASS_NAME, "qAvoV")
        #for te in type_elems:
            #print(te.text)
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
        restaurant = {'title': title, 'r_bubbles': r_bubbles, 'r_number': r_number, 'cook_type': cook_type, 'expensive': expensive}
        print('////////////////////////')
        #print(restaurant)
        restaurantsList.append(restaurant)
    #WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='onetrust-pc-dark-filter ot-fade-in']")))

    #driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]'))
    element = driver.find_element(By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]')

    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav next rndBtn ui_button primary taLnk"]'))).click()
    print("ELEMEEEENT")
    print(element.get_attribute('href'))
    #driver.find_element(By.XPATH, './/a[@class="nav next rndBtn ui_button primary taLnk"]').click()

df = pd.DataFrame(restaurantsList)
df.to_excel('yourfile.xlsx')

#elem.clear()
driver.close()