import re
import json
import requests
import numpy as np
import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup
from utils_features_scrapper import *

with open('listings.txt', 'r') as file:
    urls= [line.strip() for line in file] # Each line becomes a list element

df = pd.DataFrame()
failed_urls = pd.DataFrame()
for_loop_size = len(urls)

for i in tqdm(range(for_loop_size)):
    aux = get_car_features(urls[i])
    if aux.shape[1] > 2:
        df = pd.concat([df, aux], axis=0)
    else:
        failed_urls = pd.concat([failed_urls, aux], axis=0)

    if (i != 0) and (i%500 == 0):
        df.to_csv(f'data/partial_data/cars_features_{i}.csv', index=False)
        failed_urls.to_csv(f'data/partial_data/failed_urls_{i}.csv', index=False)

        df = pd.DataFrame()
        failed_urls = pd.DataFrame()
    
# Save final batch
i='final'
df.to_csv(f'data/partial_data/cars_features_{i}.csv', index=False)
failed_urls.to_csv(f'data/partial_data/failed_urls_{i}.csv', index=False)