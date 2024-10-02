# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:48:03 2024
Create wine profiles according to users descriptors
@author: jonma
"""

'''
WINE DESCRIPTORS:
    1- VIBRANCY (defined by acidity) 
        - fixed acidity => A higher fixed acidity value suggests a fresher or more acidic wine.
        - volatile acidity => if it is too high, it may indicate a vinegary taste.
        - citric acid => Wines with more citric acid tend to be perceived as fresher or livelier.
        - PH => A low pH (acidic) is usually associated with greater freshness and stability, while a high pH may suggest a 
        softer or less fresh wine.
        Low: Liveliness
        Medium: Live
        High: Brilliant 
        
    2- SWEETNESS (defined by sugars)
        - residual sugar => A high value implies a sweet wine, while a low value suggests a dry wine.
        Low: Dry
        Medium: Semi-Dry
        High: Sweet
        
    3- BODY (defined by alcohol & density)
        - alcohol => The higher the alcohol content, the more robust and full-bodied
        - density => A denser wine suggests more body and richness in the mouth.
        Low: Light
        Medium: Medium
        High: Full-Bodied
        
    4- NUANCE (defined by chlorides)
       - chlorides: salinity traces in the wine, which can influence a mineral sensation in the taste.
       Low: Simple
       Medium: Complex, Spicy
       High: Intense
     
    5- TANNICITY (defined by sulphates)
       - shulpathes: Higher levels may contribute to a greater sensation of dryness on the palate.
        Low: Soft
        Medium: Balanced, Structured
        High: Robust
       
'''


# READ WINES 
import os
import pandas as pd

pd.set_option("display.max_columns",None)

# OPEN FILE
path = "C:/Users/jonma/OneDrive/Escritorio/case_base_reasoning/winequality_data_set"
df_red = pd.read_csv(os.path.join(path,"winequality-red.csv"),sep=";")


# VISUALIZE & PREPROCESS DATA
df_red.info()


# REMOVE free sulfur dioxide, total sulfur dioxide & quality data. Not used in descriptors
df_red.shape
df_red = df_red.drop(["free sulfur dioxide","total sulfur dioxide","quality"],axis = 1)
df_red.shape

# CREATE COMPLEX DESCRIPTOR VALUES (BODY & VIBRANCY)

# Create new columns with same weight per each contributor
def create_new_value(row, new_col, relation_dict):
    contributors = relation_dict[new_col]
    weight = 1.0 / len(contributors)
    value = 0.0
    for val in contributors:
        value += row[val] * weight  # Access each value from the row
    return value  # Return the computed value for this row
    
# Complex descriptor relations
relation_dict = {"Body": ["alcohol", "density"],
                 "Vibrancy": ["fixed acidity","volatile acidity","citric acid","pH"]}

# Temporal body descriptor
new_col = "Body"

df_red[f"{new_col}_tmp"] = df_red.apply(lambda row: create_new_value(row, new_col, relation_dict), axis=1)

# Temporal vibrancy descriptor
new_col = "Vibrancy"
df_red[f"{new_col}_tmp"] = df_red.apply(lambda row: create_new_value(row, new_col, relation_dict), axis=1)


# SHOW DISTRIBUTION & CATEGORIZE EACH DESCRIPTOR
import matplotlib.pyplot as plt
import numpy as np


def plot_hist_with_percentiles (df, col, percent_min, percent_max):
    fig, ax = plt.subplots(figsize = (10,5))
    ax.hist(df[col])
    # Calculate percentiles
    percentiles = np.percentile(df[col], [percent_min, percent_max])
    # Add vertical lines for each percentile
    for p in percentiles:
        ax.axvline(x=p, color='red', linestyle='--', linewidth=2)
        
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    plt.show()
    
    return percentiles

def classify_data(percentiles ,col, terms):
    if col <= percentiles[0]:
        return terms[0]
    elif percentiles[0] < col <= percentiles[1]:
        return terms[1]
    else:
        return terms[2]

# categorize data
def categorize_data (df, col_list, range_dict, descriptor_dict, percent_min, percent_max):
    for col in col_list:    
       # visulize hist and 10,90 percentiles 
       percentiles =  plot_hist_with_percentiles (df, col, percent_min, percent_max) 
       
       # assign new categories according to percentiles   
       range_terms = range_dict[col]
       new_col = descriptor_dict[col]
       df[new_col] = df[col].apply(lambda x: classify_data(percentiles, x, range_terms))    
       print("\n",df_red[new_col].value_counts())
       
    return df    


# dictionary with column range terms
range_dict = {"residual sugar" : ["Dry", "Semi-Dry", "Sweet"],
     "chlorides": ["Simple", "Complex,Spicy", "Intense"],
     "sulphates": ["Soft", "Balanced,Structured", "Robust"],
     "Body_tmp": ["Light", "Medium", "Full-Bodied"],
     "Vibrancy_tmp": ["Liveliness", "Live", "Brilliant"]}

descriptor_dict = {"residual sugar" : "Sweetness",
     "chlorides": "Nuance",
     "sulphates": "Tannicity",
     "Body_tmp": "Body",
     "Vibrancy_tmp": "Vibrancy"}


# select individual descriptors and categorize
indiv_cols = ["residual sugar", "chlorides","sulphates"]
df_red = categorize_data (df_red, indiv_cols, range_dict, descriptor_dict,
                          10, 90)

# select complex descriptors columns  and categorize
tmp_cols = [col for col in df_red.columns if "tmp" in col]
df_red = categorize_data (df_red, tmp_cols, range_dict, descriptor_dict,
                          10, 90)
   
df_red.columns


# CREATE A PDF PROFILE FOR EACH WINE
# Map position to each descriptor value
descriptor_values = {"Sweetness":["Dry", "Semi-Dry", "Sweet"],
                     "Nuance": ["Simple", "Complex,Spicy", "Intense"],
                     "Tannicity": ["Soft", "Balanced,Structured", "Robust"],
                     "Body": ["Light", "Medium", "Full-Bodied"],
                     "Vibrancy":["Liveliness", "Live", "Brilliant"]}

def map_value_to_position(key, val, descriptor_values):
    return descriptor_values[key].index(val)

map_value_to_position("Nuance",  "Complex,Spicy", descriptor_values)
W   

# DRAW SPIDER GRAPHS
from math import pi

# TODO ADD DESCRIPTION CORRECTLY
# Create a radar plot for the descriptors
def create_radar_plot(data, title):
    # Prepare categories and corresponding values
    categories = ['Sweetness', 'Nuance', 'Tannicity', 'Body', 'Vibrancy']    
    values = [map_value_to_position(key, data[key], descriptor_values) for key in categories]
    values += values[:1]  # Repeat the first value at the end to close the circle

    # Calculate angles for the plot
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Start creating the radar plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 6), subplot_kw=dict(polar=True))

    # Draw one axis per variable and add labels
    ax[0].set_xticks(angles[:-1])
    ax[0].set_xticklabels(categories)

    # Draw y-labels (customizable based on your data scale)
    ax[0].set_rlabel_position(30)
    plt.yticks([0, 1, 2], ["0", "1", "2"], color="grey", size=7)
    plt.ylim(0, 2)  # Adjust depending on your value range 

    # Plot the radar chart
    ax[0].plot(angles, values, linewidth=2, linestyle='solid', label=title)
    ax[0].fill(angles, values, alpha=0.25)  # Fill area under the graph
    
    # Set title for the radar plot
    ax[0].set_title(title, size=15, color='navy', y=1.1)

    # Summary on the right side
    ax[1].axis('off')  # Turn off the axis

    # Add summary text
    summary_text = "\n".join([f"{cat}: {data[cat]} (Value: {map_value_to_position(cat, data[cat], descriptor_values)})" for cat in categories])
    ax[1].text(0.5, 0.5, summary_text, fontsize=12, ha='center', va='center', wrap=True)
   
    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.05)  # Reduce the width space between plots
    plt.tight_layout()
    plt.show()
    
    
for i in range(0,len(df_red)):
    create_radar_plot(df_red.iloc[i], title=f"Radar Plot for Wine: #{i+1}")
        
    
