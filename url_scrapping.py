import re
import time
import requests
import numpy as np
import pandas as pd

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
#url = 'https://carrosp.com.br/carros/'

price_range = [0, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 
               85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, 130000, 140000, 150000, 300000]

for i in range(13, len(price_range) - 1):
#for i in range(1):

    # Fix URL an open it
    url = f"https://carrosp.com.br/carros/todos/?revendedor=0&revendedor=S&particular=0&particular=S&tipo_id=1&marca_id=&ano1=&ano2=&zero=0&zero=S&usado=0&usado=S&kmIni=&kmFim=&precoIni={price_range[i]}&precoFim={price_range[i+1]}&idForm=formBuscaVeiculo&id=&cor_id=&combustivel_id=&distancia=100&cidadeNome=&cidade_id=&nocidade=1&"
    driver.get(url)

    # Locate the element containing the number of vehicles and extract it
    element = driver.find_element(By.CSS_SELECTOR, "p.qtde-result.font-weight-bold")
    text = element.text  
    number = int(text.split()[0]) 
    iters = round(number/21) + 1

    print(f"Price Range: R$ {price_range[i]} - R$ {price_range[i+1]} - {number} Listings - {iters} Iterations")

    car_listings = list()

    for iter in range(iters):
        # Scroll down and up to load listings
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, -1100);")

        time.sleep(3)

        #### GO HORSE

        # if iter%10 == 0: # Doing it to egt partial data so in dont lose anything
        #     elements = driver.find_elements(By.CSS_SELECTOR, "a.titulo.novajanela.mb-1")
        #     
        #     for element in tqdm(elements):
        #         href = element.get_attribute("href")
        #         if href:
        #             car_listings.append(href)

    # Repeat to process to fetch all possible data
    elements = driver.find_elements(By.CSS_SELECTOR, "a.titulo.novajanela.mb-1")
    
    print("Final fetch")
    for element in tqdm(elements):
        href = element.get_attribute("href")
        if href:
            car_listings.append(href)

    car_listings = list(set(car_listings))
    
    # Writes listings url
    with open("listings.txt", "a") as file:
        for url in car_listings:
            file.write(url + "\n")

driver.quit()   