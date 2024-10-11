# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:36:10 2024
Create user profile
@author: hrumayor
"""

import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from math import pi

pd.set_option("display.max_columns",None)

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
   
    
# EXIST USER
def exist_user (user_ids, user_id):
    return user_id in user_ids


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

'''
user_data, user_red_catalogue, user_white_catalogue =  get_specific_user_info (users_list, "12356")
user_data'''


# Each descriptor position map
descriptor_values = {"Sweetness":["Dry", "Semi-Dry", "Sweet"],
                     "Nuance": ["Simple", "Complex,Spicy", "Intense"],
                     "Tannicity": ["Soft", "Balanced,Structured", "Robust"],
                     "Body": ["Light", "Medium", "Full-Bodied"],
                     "Vibrancy":["Liveliness", "Live", "Brilliant"]}
wine_descriptors = ["Sweetness","Nuance", "Tannicity", "Body", "Vibrancy"]

def map_value_to_position(key, val):
    """
    Function that return the corresponding list position of the categorization

    Parameters:
        key (str): descriptor column name.
        val (str): descriptr column value.

    Returns:
       int position of the list
    """    
    return descriptor_values[key].index(val)


def create_radar_plot(average_df, title, save_path):
    """
    Function that plots a radar or spider plot according to average wine profile.
    
    Parameters:
        average_df (pd.DataFrame): DataFrame containing average positions for each descriptor.
        title (str): Title to assign to the plot
        save_path (str) : Path to save the plot
    Returns:
       Plots radar graph corresponding to average wine profile and saves as png.
    """  

    # Prepare categories and corresponding values
    categories = average_df['Descriptor'].tolist()
    values = average_df['Average Position'].tolist()
    values += values[:1]  # Repeat the first value at the end to close the circle

    # Calculate angles for the plot
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Start creating the radar plot
    fig, ax = plt.subplots(1, 2, figsize=(8, 8), subplot_kw=dict(polar=True))

    # Draw one axis per variable and add labels
    ax[0].set_xticks(angles[:-1])
    ax[0].set_xticklabels(categories, size=15)

    # Draw y-labels (customizable based on your data scale)
    ax[0].set_rlabel_position(30)
    plt.yticks([0, 1, 2], ["0", "1", "2"], color="grey", size=7)
    plt.ylim(0, 2)  # Adjust depending on your value range 

    # Plot the radar chart
    ax[0].plot(angles, values, linewidth=2, linestyle='solid', label=title)
    ax[0].fill(angles, values, alpha=0.25)  # Fill area under the graph
    
    # Summary on the right side
    ax[1].axis('off')  # Turn off the axis

    # Add summary text
    summary_text ='\n'.join([f"'{row['Descriptor']}': {round(row['Average Position'],2)}," for index, row in average_df.iterrows()])
    ax[1].text(0.05, 0.05, summary_text, fontsize=16, ha='center', va='center', wrap=False,
              bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.75'))

    # Set title for the radar plot
    ax[1].set_title(title, size=20, color='navy', y=0.90)

    # save file   
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(os.path.join(save_path, title + '.png'), bbox_inches='tight', pad_inches=0.5)



def visualize_wine_profile(df, title, save_path):
    
    # Applying the mapping function to each row
    df_f = pd.DataFrame()
    for descriptor in wine_descriptors:
        df_f[descriptor] = df[descriptor].apply(lambda val: map_value_to_position(descriptor, val))

  
    # Calculate average value per each descriptor based on position columns
    average_values = {
        descriptor: df_f[descriptor].mean() for descriptor in wine_descriptors
    }


    # Create a DataFrame for the average values
    average_df = pd.DataFrame.from_dict(average_values, orient='index', columns=['Average Position']).reset_index()
    average_df.rename(columns={'index': 'Descriptor'}, inplace=True)

    
    create_radar_plot(average_df, title, save_path)
    
            
# recover users_list  
users_list = get_user_list(path,wine_delivery_conf_file)    
users_list  

# recover users references
user_ids = get_users_references(users_list)   
user_ids

# get specific user data
user_id = '18050'
user_data, user_red_catalogue, user_white_catalogue = get_specific_user_info (users_list, user_id)
user_data

# red
save_path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/report"
visualize_wine_profile(user_red_catalogue, "Red_wines_profile", save_path)
# white
visualize_wine_profile(user_white_catalogue, "White_wines_profile", save_path)

def create_intro_paragraph(user_data):
    first_paragraph = ""
    total_wines = user_data['wine_qty']
    distribution = user_data["distribution"]
    
    if distribution == "equal":
        first_paragraph = f"Based on {total_wines} wines you tasted, you have no preference between red and white wines."
    else:
        who_more = distribution.split('_')[1]  # "white" or "red"
        other = "red" if who_more == "white" else "white"
        how_more = user_data['how_more']
        
        first_paragraph = (f"Based on the {total_wines} wines you tasted, you tend to prefer {who_more} wines.\n"
                           f"You have tasted {how_more} more {who_more} wines than {other} wines.\n")
    
    return first_paragraph


def zones_distribution_text(user_data):
    red_zones = {k: v for d in user_data['red_distribution'] for k, v in d.items() if "_rows" not in k}
    red_zones_l = {k: v for d in user_data['red_distribution'] for k, v in d.items() if "_rows" in k}
    white_zones = {k: int(v) for d in user_data['white_distribution'] for k, v in d.items() if "_rows" not in k}
    white_zones_l = {k: v for d in user_data['white_distribution'] for k, v in d.items() if "_rows" in k}
    

    # Ensure all keys (zones) are considered and sort them alphabetically
    all_keys = list(set(red_zones.keys()).union(white_zones.keys()))
    sorted_all_keys = sorted(all_keys, key=lambda x: x.replace('_', ''))

    # Create markdown for wine zone distribution, displaying both red and white side by side
    reds = user_data['red_wines']
    whites = user_data['white_wines']
    markdown_text = f"| Zone | Red Wines ({reds} total) | White Wines ({whites} total) |\n"
    markdown_text += "|------|-----------|-------------|\n"

    # Iterate through sorted zones and present both red and white values
    for k in sorted_all_keys:
        red_value = red_zones.get(k, 0)  # Default to 0 if zone does not exist
        white_value = white_zones.get(k, 0)  # Default to 0 if zone does not exist
        
        # Get references for red and white wines
        red_refs = red_zones_l.get(f"{k}_rows", [])  # Assuming keys are suffixed with "_rows"
        white_refs = white_zones_l.get(f"{k}_rows", [])  # Assuming keys are suffixed with "_rows"

       # Convert references to strings to avoid TypeError
        red_refs_str = ", ".join(map(str, red_refs)) if red_value > 0 else "No references."
        white_refs_str = ", ".join(map(str, white_refs)) if white_value > 0 else "No references."

        markdown_text += f"| {k} | {'No references.' if red_value == 0 else f'({red_value}) Wine refs: [{red_refs_str}]'} | {'No references.' if white_value == 0 else f'({white_value}) Wine refs: [{white_refs_str}]'} |\n"

    return markdown_text


def create_profile_text(user_data):
    title = f"Profile of the user: {user_data['user']}"
    first_paragraph = create_intro_paragraph(user_data)
    zones_distribution = zones_distribution_text(user_data)

    # Build the final markdown text for the profile
    profile_text = [
        f"# {title}\n",      
        f"{first_paragraph}", 
        "## Zones Distribution:\n",
        "Your tendency for wines by zones is as follows:\n\n",
        f"{zones_distribution}",
        "## Tasting Preferences:\n"
        "Based on wine descriptors, your wine tasting preferences are distributed as follows:\n\n"
    ]
    
    return profile_text

t = create_profile_text(user_data)
t
    

    
