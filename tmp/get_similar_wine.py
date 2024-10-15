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
import numpy as np

pd.set_option("display.max.columns",None)

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
            
    
    
# Step 2: Define a function to calculate Euclidean distance between two centroids
def euclidean_distance(centroid1, centroid2):
    return np.linalg.norm(centroid1 - centroid2)

# Function to calculate Manhattan distance
def manhattan_distance(vec1, vec2):
    return np.sum(np.abs(vec1 - vec2))

# Function to calculate Cosine similarity
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)
    
def get_nearest_wine(df, selected_row_idx , distance):
    
    # choose reference row
    selected_row = df.loc[selected_row_idx]
    cols = list(df.columns)
    
    # compute corresponding distance between selected row's centroind and all others
    df1 = df.copy()
    if distance == "euclidean":
        df1['distance'] = df1['Centroid'].apply(lambda x: euclidean_distance(selected_row['Centroid'], x))
    elif distance == "manhattan":
        df1['distance'] = df1['Centroid'].apply(lambda x: manhattan_distance(selected_row['Centroid'], x))
    else:
        df1['distance'] = df1['Centroid'].apply(lambda x: cosine_similarity(selected_row['Centroid'], x))
        
    
    # Find the row with the minimum distance (excluding the selected row itself)
    nearest_row = df1[df1.index != selected_row.name].loc[df1['distance'].idxmin()]
    
    # Convert the dictionaries to pandas Series
    to_remove = ['distance',"Cluster","Centroid"]
    a = [cols for cols in df.columns if cols not in to_remove]
    
    selected_series = pd.Series(selected_row[a])
    nearest_series = pd.Series(nearest_row[a])

   # Create the DataFrame
    solution = pd.DataFrame({
        "Selected": selected_series.values,
        "Nearest": nearest_series.values
    })
    # return selected and nearest row
    return solution



def recommend_wines (user_data):
    
    solution_red = None
    solution_white = None   
    
    if user_data["distribution"] == "equal":   # 2 recommendations one per each type
                
        # Determine red reference wine
        red = determine_favorite_zone(user_data["red_distribution"])           
        selected_red_idx = select_wine_from_favorite_zone (user_data["red_distribution"], red)
        
        # Get nearest red wine and get result in comparative way
        solution_red = get_nearest_wine(df_red, selected_red_idx , "euclidean")
               
        # Determine white reference wine
        white = determine_favorite_zone(user_data["white_distribution"])
        selected_white_idx = select_wine_from_favorite_zone (user_data["white_distribution"], white)  
        
        # Get nearest white wine and get result in comparative way
        solution_white = get_nearest_wine(df_white, selected_white_idx , "euclidean")
        
    elif user_data["distribution"] == "more_white":
        
        # Determine white reference wine
        white = determine_favorite_zone(user_data["white_distribution"])
        selected_white = select_wine_from_favorite_zone (user_data["white_distribution"], white)
        
        # Get nearest white wine and get result in comparative way
        solution_white = get_nearest_wine(df_white, selected_white_idx , "euclidean")
                    
    else:
        
        # Determine red reference wine
        red = determine_favorite_zone(user_data["red_distribution"])
        selected_red = select_wine_from_favorite_zone (user_data["red_distribution"], red)
        
        # Get nearest red wine and get result in comparative way
        solution_red = get_nearest_wine(df_red, selected_red_idx , "euclidean")
        
    return user_data["distribution"] , solution_red , solution_white
    
    
distribution, solution_red, solution_white = recommend_wines(user_data)


def create_recommendation_text(distribution, solution_red, solution_white):
    """
    Function that creates the text to add to recommendation pdf.

    Parameters:
        distribution (str): users distribution. Equal, More_white or More_red to determine if both
        solutions need to take into account or not.
        solution_red (dataframe): Selected red wine and recommended red wine visualize side by side.
        solution_white (dataframe): Selected white wine and recommended white wine visualize side by side.

    Returns:
        text to add to recommendation pdf in Markdown format.
    """    
   
    text = [
        "# Recommendations\n"
    ]
    
    if distribution == "equal":
        text.append("As you have no preference between red and white wines, I am providing a recommendation for each type.\n")
        text.append(f"## Red Wine Recommendation\n")
        text.append(f"I recommend a wine reference from {solution_red['Nearest'].iloc[-1]}: #{solution_red['Nearest'].iloc[0]}, which is very similar to the wine reference #{solution_red['Selected'].iloc[0]} from {solution_red['Selected'].iloc[-1]}.\n")
        text.append(f"## White Wine Recommendation\n")
        text.append(f"I recommend a wine reference from {solution_white['Nearest'].iloc[-1]}: #{solution_white['Nearest'].iloc[0]}, which is very similar to the wine reference #{solution_white['Selected'].iloc[0]} from {solution_white['Selected'].iloc[-1]}.\n")
    elif distribution == "more_red":
        text.append(f"## Red Wine Recommendation\n")
        text.append(f"I recommend a wine reference from {solution_red['Nearest'].iloc[-1]}: #{solution_red['Nearest'].iloc[0]}, which is very similar to the wine reference #{solution_red['Selected'].iloc[0]} from {solution_red['Selected'].iloc[-1]}.\n")
    else:
        text.append(f"## White Wine Recommendation\n")
        text.append(f"I recommend a wine reference from {solution_white['Nearest'].iloc[-1]}: #{solution_white['Nearest'].iloc[0]}, which is very similar to the wine reference #{solution_white['Selected'].iloc[0]} from {solution_white['Selected'].iloc[-1]}.\n")

    # Join text with newline characters for Markdown formatting
    rec_text = "".join(text)
    
    return rec_text
        
t = create_recommendation_text (distribution, solution_red, solution_white)
t


import matplotlib.pyplot as plt
from math import pi

# Each descriptor position map
descriptor_values = {"Sweetness":["Dry", "Semi-Dry", "Sweet"],
                     "Nuance": ["Simple", "Complex,Spicy", "Intense"],
                     "Tannicity": ["Soft", "Balanced,Structured", "Robust"],
                     "Body": ["Light", "Medium", "Full-Bodied"],
                     "Vibrancy":["Liveliness", "Live", "Brilliant"]}

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

# relation of columns and new descriptors
descriptor_dict = {"residual sugar" : "Sweetness",
     "chlorides": "Nuance",
     "sulphates": "Tannicity",
     "Body_tmp": "Body",
     "Vibrancy_tmp": "Vibrancy"}

def key_from_value(value):
    """
    Function that return the corresponding descriptor according to its value from descriptor_dict
    dictionary.

    Parameters:
        value (str): descriptor category.

    Returns:
       returns descriptor value, dictionary key
    """    
    for key,val in descriptor_dict.items():
        if val == value:
            return key

# Create a radar plot for the descriptors
def create_radar_plot(row, row2, title):
    """
    Function that plots radar or spider plot according to wine profile.
    
    Parameters:
        row (pd.DataFrame row): row corresponding to a specific wine profile.
        title (str): title to assign to the plot

    Returns:
       plots radar plot corresponding to selected wine profile
    """  

    # Prepare categories and corresponding values
    categories = ['Sweetness', 'Nuance', 'Tannicity', 'Body', 'Vibrancy']    
    values = [map_value_to_position(key, row[key]) for key in categories]
    values += values[:1]  # Repeat the first value at the end to close the circle
    
    values1 = [map_value_to_position(key, row2[key]) for key in categories]
    values1 += values1[:1]  # Repeat the first value at the end to close the circle

    # Calculate angles for the plot
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Start creating the radar plot
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), subplot_kw=dict(polar=True))  # Adjust figure size

    # Draw one axis per variable and add labels
    ax[0].set_xticks(angles[:-1])
    ax[0].set_xticklabels(categories, size=15)

    # Draw y-labels (customizable based on your data scale)
    ax[0].set_rlabel_position(30)
    plt.yticks([0, 1, 2], ["0", "1", "2"], color="grey", size=7)
    plt.ylim(0, 2)  # Adjust depending on your value range 

    # Plot the radar chart
    ax[0].plot(angles, values, linewidth=2, linestyle='solid', label="reference")
    ax[0].fill(angles, values, alpha=0.25)  # Fill area under the graph
    ax[0].plot(angles, values1, linewidth=2, linestyle='solid', label="nearest")
    ax[0].fill(angles, values1, alpha=0.25)  # Fill area under the graph
    
    # Summary on the right side
    ax[1].axis('off')  # Turn off the axis

    # Add summary text, moving it further to the left
    summary_text = "\n".join([f"$\\bf{{{cat}}}$:\n{row[cat]} vs {row2[cat]} \n" + f"(V:{round(row[key_from_value(cat)],2)}) vs (V:{round(row2[key_from_value(cat)],2)})"
                               for i, cat in enumerate(categories)])
    ax[1].text(-0.1, 0.08, summary_text, fontsize=16, ha='left', va='center', wrap=True) 
    
    # Adjust layout for minimal spacing
    plt.subplots_adjust(top=0.85, wspace=0.01, left=0.01, right=0.99)  # Minimal horizontal spacing
    
    # Set title for the radar plot
    fig.suptitle(title, size=20, color='navy', y=0.95) 
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()


    
title = f"Taste comparation between wines ref: #{solution_red['Selected'][0]} and #{solution_red['Nearest'][0]} ({solution_red['Nearest'][len(solution_red)-1]})"
create_radar_plot(df_red.iloc[solution_red["Selected"][0]], df_red.iloc[solution_red["Nearest"][0]],
                  title)