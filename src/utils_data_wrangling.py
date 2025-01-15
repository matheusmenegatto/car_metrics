import ast
import unicodedata
import numpy as np
import pandas as pd

def get_spread_info(df, col, all_values):
    check_cols = ['year', 'engine', 'transmission', 'fuel_type', 'body_type', 'color']
    if col not in check_cols:
        raise(ValueError(f"col must be one of {check_cols}"))
    
    df = df.copy()

    df[f'spread_{col}'] = np.nan

    if col != 'engine':
        df[f'spread_{col}'] = np.where(df['engine'].isin(all_values), df['engine'], df[f'spread_{col}'])
    if col != 'valves':
        df[f'spread_{col}'] = np.where(df['valves'].isin(all_values), df['valves'], df[f'spread_{col}'])
    if col != 'transmission':
        df[f'spread_{col}'] = np.where(df['transmission'].isin(all_values), df['transmission'], df[f'spread_{col}'])
    if col != 'fuel_type':
        df[f'spread_{col}'] = np.where(df['fuel_type'].isin(all_values), df['fuel_type'], df[f'spread_{col}'])
    if col != 'body_type':
        df[f'spread_{col}'] = np.where(df['body_type'].isin(all_values), df['body_type'], df[f'spread_{col}'])
    if col != 'color':
        df[f'spread_{col}'] = np.where(df['color'].isin(all_values), df['color'], df[f'spread_{col}'])
            
    df[f'spread_{col}'] = np.where(df['doors'].isin(all_values), df['doors'], df[f'spread_{col}'])

    return df

def get_spread_mileage_info(df):
    df = df.copy()
    df['spread_mileage'] = np.nan

    for col in ['engine', 'transmission', 'fuel_type', 'body_type', 'color', 'doors', 'valves']:
        df['spread_mileage'] = np.where((df[col].str.endswith(('KM', 'KM KM'))) == True, df[col], df['spread_mileage'])

    return df

def fix_string(text):
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    text = text.replace(' ', '_')
    return text

def fix_items(row):
    return str([fix_string(item) for item in ast.literal_eval(row['other_features'])])

def check_feature(row, feature):
    return 1 if feature in ast.literal_eval(row['other_features']) else 0