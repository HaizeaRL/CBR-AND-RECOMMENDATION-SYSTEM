# wine recommendation functions
import random
import numpy as np
import pandas as pd
import os

# Functions
def determine_favorite_zone (zones):
    """
    Function that determines which wine zone is users favorite.
    
    Parameters:
        zones : list of wines distributed by zone for user.
    Returns:
        users favorite zone. Example: "Zone_A".
    """    

    z = ""
    max_v = 0.0
    for zone in zones:
        for k, v in zone.items():
            if "_row" not in k and  v > max_v:
                max_v = v
                z = k
    return z

def select_wine_from_favorite_zone(zones, favorite_zone):
    """
    Function that select one of the wines as reference from users favorite wine zone.
    
    Parameters:
        zones : list of wines distributed by zone for user.
        favorite_zone (str) : zone to filter from all zones to select a wine for this list as reference.
    Returns:
        Returns randomly selected wine from favorite zone.
    """    
    for zone in zones:
        for k, v in zone.items():
            if favorite_zone+"_rows" == k:
                return (v[random.randint(0, len(v)-1)])
            

def euclidean_distance(vec1, vec2):
    """
    Function that calculates euclidean distance of two centroids.

    Parameters:
        vec1 : centroid data of a cluster.
        vec2 : centroid data of other cluster.

    Returns:
        euclidean distance between both cluster centroids.
    """    
    return np.linalg.norm(vec1 - vec2)

def manhattan_distance(vec1, vec2):
    """
    Function that calculates manhattan distance of two centroids.

    Parameters:
        vec1 : centroid data of a cluster.
        centroid2 : centroid data of other cluster.

    Returns:
        manhattan distance between both cluster centroids.
    """    
    return np.sum(np.abs(vec1 - vec2))


def cosine_similarity(vec1, vec2):
    """
    Function that calculates cosine similarity distance of two centroids.

    Parameters:
        vec1 : centroid data of a cluster.
        centroid2 : centroid data of other cluster.

    Returns:
        cosine similarity distance between both cluster centroids.
    """    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def get_nearest_wine(df, selected_row_idx , distance):
    """
    Function that calculates the similarity of indicated wine.

    Parameters:
        df (dataframe) : wine catalogue to select nearest wine.
        selected_row_idx (int) : wine row to used as reference.
        distance (str): function to calculate distance. Euclidean, manhattan or cosine_similarity.

    Returns:
        selected wine and its rearest as a single dataframe
    """    
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
    rest_of_columns = [cols for cols in df.columns if cols not in to_remove] # only interested columns
    
    selected_series = pd.Series([selected_row.name] + list(selected_row[rest_of_columns])) # add index as first element
    nearest_series = pd.Series([nearest_row.name] + list(nearest_row[rest_of_columns])) # add index as first element

   # Create the DataFrame
    solution = pd.DataFrame({
        "Selected": selected_series.values,
        "Nearest": nearest_series.values
    })
    # return selected and nearest row
    return solution

def recommend_wines (user_data,  user_red_cat, user_white_cat):
    """
    Function that select reference wine and obtain similar wine as recommendation.

    Parameters:
        user_data : users wine preferences. User wine profile.
        user_red_cat: users red wine catalogue.
        user_white_cat: users white wine catalogue.

    Returns: 
        user_data["distribution"] (str): users distribution. Equal, More_white or More_red to determine if both
        solution need to take into account or not.
        solution_red (dataframe) : Selected red wine and recommended red wine visualize side by side.
        solution_white(dataframe) : Selected white wine and recommended white wine visualize side by side.
    """    
    
    solution_red = None
    solution_white = None   
    
    if user_data["distribution"] == "equal":   # 2 recommendations one per each type
                
        # Determine red reference wine
        red = determine_favorite_zone(user_data["red_distribution"])           
        selected_red_idx = select_wine_from_favorite_zone (user_data["red_distribution"], red)
        
        # Get nearest red wine and get result in comparative way
        solution_red = get_nearest_wine(user_red_cat, selected_red_idx , "euclidean")
               
        # Determine white reference wine
        white = determine_favorite_zone(user_data["white_distribution"])
        selected_white_idx = select_wine_from_favorite_zone (user_data["white_distribution"], white)  
        
        # Get nearest white wine and get result in comparative way
        solution_white = get_nearest_wine(user_white_cat, selected_white_idx , "euclidean")
        
    elif user_data["distribution"] == "more_white":
        
        # Determine white reference wine
        white = determine_favorite_zone(user_data["white_distribution"])
        selected_white_idx = select_wine_from_favorite_zone (user_data["white_distribution"], white)
        
        # Get nearest white wine and get result in comparative way
        solution_white = get_nearest_wine(user_white_cat, selected_white_idx , "euclidean")
                    
    else:
        
        # Determine red reference wine
        red = determine_favorite_zone(user_data["red_distribution"])
        selected_red_idx = select_wine_from_favorite_zone (user_data["red_distribution"], red)
        
        # Get nearest red wine and get result in comparative way
        solution_red = get_nearest_wine(user_red_cat, selected_red_idx , "euclidean")
        
    return user_data["distribution"] , solution_red , solution_white


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
   
    intro_text = ""
    paragraph1 = ""
    paragraph2 = ""
    # complete text in each case
    if distribution == "equal":
        intro_text = "As you have no preference between red and white wines, I am providing a recommendation for each type.\n\n"
        paragraph1 = f"I recommend a red wine reference from {solution_red['Nearest'].iloc[-1]}: #{solution_red['Nearest'].iloc[0]}, which is very similar to the red wine reference #{solution_red['Selected'].iloc[0]} also from {solution_red['Selected'].iloc[-1]}.\n"
        paragraph2 = f"I recommend a white wine reference from {solution_white['Nearest'].iloc[-1]}: #{solution_white['Nearest'].iloc[0]}, which is very similar to the white wine reference #{solution_white['Selected'].iloc[0]} also from {solution_white['Selected'].iloc[-1]}.\n"
    elif distribution == "more_red":
        intro_text = "Based on your wine preferences.\n\n"
        paragraph1 = f"I recommend a red wine reference from {solution_red['Nearest'].iloc[-1]}: #{solution_red['Nearest'].iloc[0]}, which is very similar to the red wine reference #{solution_red['Selected'].iloc[0]} also from {solution_red['Selected'].iloc[-1]}.\n"
    else:
        intro_text = "Based on your wine preferences.\n\n"
        paragraph1 = f"I recommend a white wine reference from {solution_white['Nearest'].iloc[-1]}: #{solution_white['Nearest'].iloc[0]}, which is very similar to the white wine reference #{solution_white['Selected'].iloc[0]} also from {solution_white['Selected'].iloc[-1]}.\n"
    
    # markdown type text structure
    text = [
        "# Recommendation\n",
         intro_text,
         paragraph1,
         paragraph2,
         "Their whine profiles are shown below."
    ]
    
    return text
        
