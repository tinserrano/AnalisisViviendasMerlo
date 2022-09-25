from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = '/Users/tinpenas/Downloads/chromedriver.exe'

driver = webdriver.Chrome(ChromeDriverManager().install())


item_address_list = []
address_zone_list = []
descripciones = []
price_list = []
slug_list = []

#páginas totales
pages = 38


for page_number in range(1, pages):
    page_url = f'https://www.inmobiliarialoyola.com/home/properties/page:{page_number}/sort:Property.argenprop_puntos/direction:desc'
    driver.get(page_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    description = soup.find_all(class_='description')
    for i in range(len(description)):
        descripciones.append(description[i].get_text())  

    item_address = soup.find_all(class_='item address')
    for i in range(len(item_address)):
        item_address_list.append(item_address[i].get_text().replace("\n",""))

    address_zone = soup.find_all(class_='address_zone')
    for i in range(len(address_zone)):
        address_zone_list.append(address_zone[i].get_text())

    price = soup.find_all(class_='price')
    for i in range(len(price)):
        price_list.append(price[i].get_text())

    slug = soup.find_all(class_='slug')
    for i in range(len(slug)):
        slug_list.append(slug[i].get_text().replace(' Cód.: ',''))

    time.sleep(4)
    #next = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/ul/li[7]/a")
    #next.click()
    #time.sleep(3)


df2 = pd.DataFrame({
        'Price':price_list, 
        'Descripcion':descripciones, 
        'ItemAddressList':item_address_list, 
        'Zona':address_zone_list,
        'Codigo':slug_list})

df2.to_csv(r'/Users/tinpenas/RealStateMerlo/list.csv', index=None, header=True)
driver.close()

