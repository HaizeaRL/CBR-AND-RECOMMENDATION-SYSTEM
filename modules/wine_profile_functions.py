# wine profiling functions

import os
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Complex descriptors relations
complex_relation_dict = {"Body": ["alcohol", "density"],
                 "Vibrancy": ["fixed acidity","volatile acidity","citric acid","pH"]}

# dictionary with column and new categorization relation
range_dict = {"residual sugar" : ["Dry", "Semi-Dry", "Sweet"],
     "chlorides": ["Simple", "Complex,Spicy", "Intense"],
     "sulphates": ["Soft", "Balanced,Structured", "Robust"],
     "Body_tmp": ["Light", "Medium", "Full-Bodied"],
     "Vibrancy_tmp": ["Liveliness", "Live", "Brilliant"]}

# relation of columns and new descriptors
descriptor_dict = {"residual sugar" : "Sweetness",
     "chlorides": "Nuance",
     "sulphates": "Tannicity",
     "Body_tmp": "Body",
     "Vibrancy_tmp": "Vibrancy"}

# Each descriptor position map
descriptor_values = {"Sweetness":["Dry", "Semi-Dry", "Sweet"],
                     "Nuance": ["Simple", "Complex,Spicy", "Intense"],
                     "Tannicity": ["Soft", "Balanced,Structured", "Robust"],
                     "Body": ["Light", "Medium", "Full-Bodied"],
                     "Vibrancy":["Liveliness", "Live", "Brilliant"]}

# wine descriptors
wine_descriptors = ["Sweetness","Nuance", "Tannicity", "Body", "Vibrancy"]


def create_new_value(row, descriptor):
    """
    Function that is responsible to calculate complex descriptors new values.
    Example: body is composed by alcohol and density values. Each contributor has same weight 1/2.
    Each contibutor have same weight. 

    Parameters:
        row (pd.DataFrame row): row to calculate new value.
        descriptor (str): descriptor to find in the dictionary. 

    Returns:
        value: return the corresponding calculated value for each row.
    """    
    contributors = complex_relation_dict[descriptor] # get contributors columns
    weight = 1.0 / len(contributors) # same weight to each contributor
    value = 0.0 # initialize
    for val in contributors:
        value += row[val] * weight  # Access each value from the row
    return value  # Return the computed value for this row


def plot_hist_with_percentiles (df, col, percent_min, percent_max):
    """
    Function that plot selected columns histogram with defined percentile limits as vertical red lines.

    Parameters:
        df (pd.DataFrame): dataframe to filter value
        col (str): column to plot
        percent_min (int): min percentile value to plot vertical red line.
        percent_max (int): max percentile value to plot vertical red line.

    Returns:
        Plot corresponding histogram and returns:
        percentiles: specified percentile values of selected column
    """    
    percentiles = np.percentile(df[col], [percent_min, percent_max]) 
    '''fig, ax = plt.subplots(figsize = (10,5))
    ax.hist(df[col])

    # Calculate percentiles & add vertical lines for each percentile
    percentiles = np.percentile(df[col], [percent_min, percent_max])    # 
    for p in percentiles:
        ax.axvline(x=p, color='red', linestyle='--', linewidth=2)
        
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    #plt.show()'''
    
    return percentiles # return percentile values

def classify_data(percentiles, col, terms):
    """
    Function that categorized especified column by terms provided according to percentile values.

    Parameters:
        percentiles (list): percentile limits
        col (str): column to apply categorization
        terms (list): list of values to use to categorize the new value

    Returns:
       new categorization according to percentile values
    """    
    if col <= percentiles[0]: # less than minimum percentile value
        return terms[0] # assign first term of the list
    elif percentiles[0] < col <= percentiles[1]: # between both percentile values
        return terms[1] # assign second term of the list
    else: # greater than maximum percentile
        return terms[2] # assign third term of the list
    

def categorize_data (df, col_list, percent_min, percent_max):
    """
    Function that categorized especified columns by terms of provides percentile values.

    Parameters:
        df (pd.DataFrame): dataframe to apply the categorization.
        col_list (list(str)): list of columns to be categorized.
        percent_min (int): min percentile value, to classify the categorization.
        percent_max (int): max percentile value, to classify the categorization.

    Returns:
       new categorization according to percentile values
    """    
    for col in col_list:    
       # visulize hist and 10,90 percentiles 
       percentiles =  plot_hist_with_percentiles (df, col, percent_min, percent_max) 
       
       # assign new categories according to percentiles   
       range_terms = range_dict[col]
       new_col = descriptor_dict[col]
       df[new_col] = df[col].apply(lambda x: classify_data(percentiles, x, range_terms))    
       #print("\n",df[new_col].value_counts())
       
    return df   

def wine_profiling(path, filename):
    """
    Function that creates wine profile

    Parameters:
        path (str): path to data.
        filename (str): filename to use to create profiles.
    Returns:
       NULL
       saves new _categorized files with wine profiles.
    """    
    # open wine data
    filename_root = filename.split(".")[0]
    df = pd.read_csv(os.path.join(path,filename),sep=";")

    # remove no used data
    no_used_cols = ["free sulfur dioxide","total sulfur dioxide","quality"]
    df = df.drop(no_used_cols,axis = 1)

    # detect if exist duplicates & remove if any
    duplicate_indices = df[df.duplicated(keep=False)].index
    if len(duplicate_indices) >0:
        df = df.drop(duplicate_indices).reset_index(drop=True)

    # create complex descriptors (temporal new values used to categorized)
    new_col = "Body"
    df[f"{new_col}_tmp"] = df.apply(lambda row: create_new_value(row, new_col), axis=1)

    new_col = "Vibrancy"
    df[f"{new_col}_tmp"] = df.apply(lambda row: create_new_value(row, new_col), axis=1)

    # categorize data
    # select individual descriptors and categorize
    indiv_cols = ["residual sugar", "chlorides","sulphates"]
    df = categorize_data (df, indiv_cols, 10, 90)

    # select complex descriptors columns  and categorize
    tmp_cols = [col for col in df.columns if "tmp" in col]
    df = categorize_data (df, tmp_cols, 10, 90)

    # create folder to save data
    data_path = path.rsplit('files', 1)[0]  # Get the part before 'files'
    new_data_path = os.path.join(data_path, "data")  # Create new path to data folder
    os.makedirs(new_data_path, exist_ok=True)

    # save information in new data folder
    new_filename = f"{filename_root}_categorized.csv"
    df.to_csv(os.path.join(new_data_path, new_filename),index =False)


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


