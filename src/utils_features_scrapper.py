import re
import json
import requests
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

def _get_listing_id(soup):
    script_tag = soup.find('script', string=re.compile(r'var infoVeiculo'))
    match = re.search(r'var infoVeiculo = ({.*?});', script_tag.string)
    return json.loads(match.group(1))['id']

def _get_general_features(soup):
    text = soup.find("div", class_="d-flex flex-wrap w-100 mt-3").p.get_text(strip=True)
    return_list = [feature.strip() for feature in text.split("|")]
    return_list = (return_list + [np.nan] * 5)[:5]
    
    return return_list

def _get_header_info(soup):
    h1 = soup.find("h1", class_="text-uppercase desktop")

    maker = h1.contents[0].strip()
    model = h1.find("span").get_text(strip=True)
    other_info = h1.find("span", class_="gray").get_text(strip=True)
    other_info = other_info.replace("\xa0", " ")

    other_info = [feature.strip() for feature in other_info.split(' ')]
    return_list = [maker, model]
    return_list = return_list + other_info

    return_list = (return_list + [np.nan] * 5)[:5]

    return return_list

def _get_li_features(soup):
    features = soup.find_all("li", class_="list-style-none mb-3")
    return [feature.get_text(strip=True) for feature in features]

def _get_seller_description(soup):
    text = soup.find("p", itemprop="description")
    return text.get_text(separator="\n", strip=True).replace("\n", " ") if text else np.nan
    
def _get_image(soup):
    text = soup.find('meta', {'property': 'og:image'})
    return text.get('content') if text else np.nan
    
def _get_city(soup):
    text = soup.find("p", class_="mb-0 mt-3 d-flex align-items-baseline")
    return text.get_text(strip=True) if text else np.nan

def _get_price(soup):
    text = soup.find('p', class_='mb-0 pr-2 text-color-1')
    return text.get_text(strip=True) if text else np.nan

def _get_year(soup):
    text = soup.find('p', class_='mb-0 px-2 meio')
    return text.get_text(strip=True) if text else np.nan

def get_car_features(url):
    try: 
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, 'html.parser')

        general_features = _get_general_features(soup)
        header_info = _get_header_info(soup)
        li_features = _get_li_features(soup)
        seller_description = _get_seller_description(soup)
        image = _get_image(soup)
        year = _get_year(soup)
        city = _get_city(soup)
        price = _get_price(soup)

        features_dict = {
            'id': _get_listing_id(soup),
            'title': soup.title.string,
            'seller_description': seller_description,
            'link': soup.find('meta', {'property': 'og:url'}).get('content'), 
            'image': image,
            'maker': header_info[0],
            'model': header_info[1],
            'year': year,
            'engine': header_info[2],
            'valves': header_info[3],
            'transmission': general_features[0],
            'fuel_type': general_features[1],
            'body_type': general_features[2],
            'doors': header_info[4],
            'color': general_features[3],
            'mileage': general_features[4],
            'other_fatures': li_features,
            'city': city,
            'price': price,
        }

        return pd.DataFrame([features_dict])
    
    except Exception as e:
        return pd.DataFrame({
            'url': [url],
            'error': [e]
        })
