# user wine distribution functions
import random
import pandas as pd
import os
import json

def total_wine_distribution ():
    """
    Function that randomly select if an user has equal red and white wines or not.

    Returns:
       str: indicate whether the user has more reds, more white or equal quantity of wines.
    """   
    choices = ["more_red", "more_white", "equal"]
    return choices[random.randint(0, 2)]
    
def wine_quantity():
    """
    Function that randomly selects how many wines has each user
    limits (5, 20)

    Returns:
       int: indicate users total wine quantity
    """   
    return random.randint(5, 20)

def how_more():
    """
    Function that randomly selects how many wines more have the user. 
    Only if "more_red" or "more_white" is selected.
    limits (1, 5)

    Returns:
       int: indicate how more wines has the user.
    """   
    return random.randint(1, 5)

def isOdd (qty):
    """
    Function that determines whether total wine quantity is odd or not.

    Parameters:
        qty (int): total wine quantity of user

    Returns:
       boolean: indicate whether users total wine quantity is odd or not.
    """
    return qty % 2 != 0

def calculate_distribution(qty, qty2):
    """
    Function that based on total wine quantity and how many more needs to have in one of the 
    wines distribute each wines quantitites.
    a + b = qty
    a - b = qty2
    
    a = qty - b
    b = (qty - qty2) / 2  # if (qty - qty2) is odd adjust qty to has an integer as a result.

    Parameters:
        qty (int): total wine quantity of user
        qty2 (int): how many more

    Returns:
       qty: new total quantity. If (qty - qty2) is odd qty+=1 as a result.
       minin: minimum value to assign to corresponding less wine side.
       maxim: maximum value to assign to corresponding more wine side.
    """ 
    minin = 0
    maxim = 0
    if isOdd((qty-qty2)):
        qty = qty + 1
        minin = int((qty-qty2) / 2)
        maxim = int(qty - minin)
    else:
        minin = int((qty-qty2) / 2)
        maxim = int(qty - minin)      
    return qty, minin, maxim


def wine_distribution (choice, qty):
    """
    Function that distributes red and white wine cuantities depending of 
    randomly selected option

    Parameters:
        choice (str): randomly selected more reds, more white or equal quantity of wines.
        qty (int): randomly selected total user wines.

    Returns:
       qty: new total quantity. If (qty - qty2) is odd qty+=1 as a result.
       qty2: randomly selected how many more wines. Only if "more_red" or "more_white" is selected. 
       minin: minimum value to assign to corresponding less wine side.
       maxim: maximum value to assign to corresponding more wine side.
    """ 
    red_wines = 0
    white_wines = 0
    qty2 = 0 # how many more
    odd = isOdd(qty) # total quantity 
    if odd:
        qty = (qty + 1)    
    
    if choice == "equal":
        red_wines = qty / 2 # mid value each
        white_wines = qty / 2
     
    else:        
        qty2 = how_more()  # select how many more randomly
        qty, minin, maxim = calculate_distribution(qty, qty2) # calculate corresponding values
        # assign max and min values according to maximum and minimum side of wines
        if choice == "more_red":
            red_wines = maxim
            white_wines = minin
        else:
            white_wines = maxim
            red_wines = minin

    # return updated values   
    return qty, qty2, red_wines, white_wines

def wine_zone_distribution (n_clusters, tot_wines):
    """
    Function that select how many wines per each cluster (or zone)
    need to be selected. 
    The selection is done in a balanced way.

    Parameters:
        n_clusters (int): number of wine zones or clusters.
        tot_wines (int): total wine quantity to select per zone.

    Returns:
       zones: a list of how many wines need to select per zone or cluster. 
    """ 
    # intialize zones
    zones = [{f"Zone_{chr(i)}": 0} for i in range(65, 65 + n_clusters)]

    # Calculate base distribution and remainder
    base_wine_per_zone = tot_wines // n_clusters
    remainder_wines = tot_wines % n_clusters

    # Distribute base amount per zone
    for zone_dict in zones:
        for key in zone_dict:
            zone_dict[key] = base_wine_per_zone

    # Distribute remainder randomly across zones
    while remainder_wines > 0:
        chosen_zone = random.choice(zones)
        for key in chosen_zone:
            chosen_zone[key] += 1
        remainder_wines -= 1
    return zones



def wine_delibery(df, pattern):
    """
    Function that select wines per each cluster (or zone) from catalogue following 
    selecting distribution pattern.
    
    Parameters:
        df (dataframe): wine catalogue
        pattern (list[dict]): a list

    Returns:
       zones: a list of selected wines per zone or cluster following distribution pattern.
    """ 
    # initialize list
    new_distribution = []
  
    # iterate pattern and select corresponding rows
    for zones_dict in pattern:
        zone_name = list(zones_dict.keys())[0] 
        zone_qty = int(list(zones_dict.values())[0])
        
        # filter data by zone_name & selec data
        zone_df = df[df["Zone"] == zone_name]   
        if len(zone_df) >= zone_qty:
            selected_indices = random.sample(zone_df.index.tolist(), zone_qty)
        else:
            selected_indices = zone_df.index.tolist()  # If there are not enough, select all
        # create dictionary
        n_d = {}
        n_d[zone_name] = selected_indices
        # append new assginations
        new_distribution.append(n_d)
    return new_distribution

def wine_assginations (wine_distribution, row_distribution):
    """
    Function that sum in a combined list:
    - The list of how many wines need to select per zone or cluster (pattern).
    - The list of select wines per each cluster (or zone) from catalogue following the pattern.
    
    Parameters:
        wine_distribution (list[dict]): list of how many wines need to select per zone or cluster 
        row_distribution (list[dict]):list of select wines per each cluster (or zone)

    Returns:
       combined_list: a list of selected wines saving the pattern and selected row per cluster (or zone).
    """ 
    # initialilze list
    combined_list = []

    # Loop through the distributions
    for dist, r_dist in zip(wine_distribution, row_distribution):
        # get zone name
        zone_name = list(dist.keys())[0]
        
        # new dictionary entry
        combined_entry = {
            zone_name: dist[zone_name],             # distribution value
            f"{zone_name}_rows": r_dist[zone_name]  # rows
        }
        
        # add entry
        combined_list.append(combined_entry)
    return combined_list

def save_dict_list_json(path, user_list):
    """
    Function that saves as json users wine delivery configuration.

    Parameters:
        path (str): data root path to save configuration
        user_list (list[dict]): list of dictionaries to save as json.

    Returns:
       Null
       Saves data as json.
    """ 

    with open(os.path.join(path,"users_wine_delivery_conf.json"), 'w') as json_file:
        json.dump(user_list, json_file)

    
def wine_delibery_conf (path, filename1, filename2):
    """
    Function that creates users and save each users wine delivery configuration
    
    Parameters:
        path (str): wines catalogue root path
        filename1 (str): red wines catalogue filename
        filename2 (str): white wines catalogue filename

    Returns:
       user_list: a list of users and its wine delivery configuration
    """ 

    # load wine catalogues 
    df_red = pd.read_parquet(os.path.join(path, filename1+".parquet"), engine ="pyarrow")
    df_white = pd.read_parquet(os.path.join(path, filename2+".parquet"), engine ="pyarrow")

    # Create users configuration 
    user_list = []
    for i in range(0, random.randint(5,20)):
        d = {}
        choice = total_wine_distribution()
        qty = wine_quantity()
        d["user"]= ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 5)])
        d["distribution"] = choice
        qty, qty2, red_wines, white_wines = wine_distribution (choice, qty)
        d["wine_qty"] = qty
        d["how_more"] = qty2
        d["red_wines"] = red_wines
        d["white_wines"] = white_wines
        red_clusters = len(df_red["Cluster"].unique())
        red_distr = wine_zone_distribution (red_clusters, d["red_wines"])   
        red_distr_delivery = wine_delibery(df_red, red_distr)  
        d["red_distribution"] = wine_assginations(red_distr, red_distr_delivery)        
        white_clusters = len(df_white["Cluster"].unique())
        white_distr = wine_zone_distribution (white_clusters, d["white_wines"])
        white_distr_delivery = wine_delibery(df_white, white_distr)  
        d["white_distribution"] = wine_assginations(white_distr, white_distr_delivery)
        user_list.append(d)
    
    return user_list

