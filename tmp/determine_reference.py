# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:00:08 2024
Function that determines which is the reference wine to find its similar.
@author: hrumayor
"""

import os
import pandas as pd
import json
import random

pd.set_option("display.max_columns",None)

# load wine catalogues 
path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/data"
wine_delivery_conf_file = "users_wine_delivery_conf.json"
red_filename = "red_wines_clustered"
white_filename = "white_wines_clustered"

df_red = pd.read_parquet(os.path.join(path, red_filename+".parquet"), engine ="pyarrow")
df_white = pd.read_parquet(os.path.join(path, white_filename+".parquet"), engine ="pyarrow")

# RECOVER USERS LIST
def get_user_list(path, json_file):
    json_file_path = os.path.join(path,json_file)
    
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)
    
# GET USERS REFERENCES
def get_users_references(users_list):
    if len(users_list)> 0:
        return [x["user"] for x in users_list]
    
# GET SPECIFIC WINES
def get_specified_rows(zones):
    
    # List to store the row indices
    row_idx = []

    # Loop through each zone and extract the row indices
    for zone in zones:
        for key, value in zone.items():
            if '_rows' in key:  # Check if the key ends with '_rows'
                row_idx.extend(value)
    return row_idx

            
def get_specific_wines(df, wine_distr):
    
    # get wine rows
    wines_rows = get_specified_rows(wine_distr)
    
    #filter & retrun user wine catalogue
    return df.iloc[wines_rows]

# GET SPECIFIC USER DATA
def get_specific_user_info (users_list, user_id):
    
    # initialize data
    user_data = None
    user_red_catalogue = None
    user_white_catalogue = None
    
    # get specific user's data
    user_info = [x for x in users_list if x["user"] == user_id]
    if len(user_info) == 1:
        
        user_data = user_info[0]
        
        print(f"\n\t\tUser: '{user_data['user']}'")
        print(f"\t\tTotal wines: {user_data['wine_qty']}")
        print(f"Red Wines: {user_data['red_wines']} \t| \t White Wines: {user_data['white_wines']}")

        red_zones = {k: v for d in user_data['red_distribution'] for k, v in d.items() if "_rows" not in k}
        white_zones = {k: int(v) for d in user_data['white_distribution'] for k, v in d.items() if "_rows" not in k}
        text = ""

        # Ensure that all keys are considered
        all_keys = list(set(red_zones.keys()).union(white_zones.keys()))
        sorted_all_keys = sorted(all_keys, key=lambda x: x.replace('_', ''))

        for k in sorted_all_keys:
            red_value = red_zones.get(k, 0)  # 0 if key doesn't exit. 
            white_value = white_zones.get(k, 0)  # 0 if key doesn't exit. 
            text += f"\t{k}: {red_value} \t| \t\t {k}: {white_value}\n"

        print(text)
        
        # filter and obtain user wine catalogue to create profile
        user_red_catalogue = get_specific_wines(df_red, user_info[0]["red_distribution"])
        user_white_catalogue = get_specific_wines(df_white, user_info[0]["white_distribution"])
    
    return user_data, user_red_catalogue, user_white_catalogue
    
# recover users_list  
users_list = get_user_list(path,wine_delivery_conf_file)    
users_list  

# recover users references
user_ids = get_users_references(users_list)   
user_ids

# get specific user data
user_id = '85725'
user_data, user_red_catalogue, user_white_catalogue = get_specific_user_info (users_list, user_id)
user_data


zones = user_data["white_distribution"]



def determine_favorite_zone (zones):
    z = ""
    max_v = 0.0
    for zone in zones:
        for k, v in zone.items():
            if "_row" not in k and  v > max_v:
                max_v = v
                z = k
    return z

def select_wine_from_favorite_zone(zones, favorite_zone):
    for zone in zones:
        for k, v in zone.items():
            if favorite_zone+"_rows" == k:
                return (v[random.randint(0, len(v)-1)])
            
    
    
# Determine similar to what wine want to recommend. 
for users in users_list:
    
    if users["distribution"] == "equal":
        red = determine_favorite_zone(users["red_distribution"])           
        selected_red = select_wine_from_favorite_zone (users["red_distribution"], red)
        white = determine_favorite_zone(users["white_distribution"])
        selected_white = select_wine_from_favorite_zone (users["white_distribution"], white)  
        
    elif users["distribution"] == "more_white":
        white = determine_favorite_zone(users["white_distribution"])
        selected_white = select_wine_from_favorite_zone (users["white_distribution"], white)
     
    else:
        red = determine_favorite_zone(users["red_distribution"])
        selected_red = select_wine_from_favorite_zone (users["red_distribution"], red)
        