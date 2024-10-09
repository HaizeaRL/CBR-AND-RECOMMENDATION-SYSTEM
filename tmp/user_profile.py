# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:36:10 2024
Create user profile
@author: hrumayor
"""

import os
import pandas as pd
import json

path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/data"
red_filename = "red_wines_clustered"
white_filename = "white_wines_clustered"
wine_delivery_conf_file = "users_wine_delivery_conf.json"


# load wine catalogues 
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
  

# GET SPECIFIC USER DATA
def get_specific_user_info (users_list, user_id):
    
    # get specific data
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
        all_keys.reverse()

        for k in all_keys:
            red_value = red_zones.get(k, 0)  # 0 if key doesn't exit. 
            white_value = white_zones.get(k, 0)  # 0 if key doesn't exit. 
            text += f"\t{k}: {red_value} \t| \t\t {k}: {white_value}\n"

        print(text)
    return user_data
   
    
# EXIST USER
def exist_user (user_ids, user_id):
    return user_id in user_ids
    
            
# recover users_list  
users_list = get_user_list(path,wine_delivery_conf_file)    
users_list  

# recover users references
user_ids = get_users_references(users_list)   
user_ids

# get specific user data
user_id = '18050'
a = get_specific_user_info (users_list, user_id)
a

b = get_specific_user_info (users_list, "12356")
b

red_list= []
red_zones = {v for d in a['red_distribution'] for k, v in d.items() if "_rows" in k}


