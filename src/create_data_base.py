import os
import pandas as pd
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import wine_profile_functions as wpf
from modules import wine_clustering_functions as wcf
from modules import user_wine_distribution_functions as uwdf

# Check if the output directory exists
if os.path.exists("../files"):
    # 1- CREATE WINE PROFILES & SAVE    
    print("CREATING WINE PROFILES")     
    # Create wine profiles for red and white wines
    wpf.wine_profiling("../files", "red_wines.csv")  # red wines
    wpf.wine_profiling("../files", "white_wines.csv")  # white wines

# Check if the data directory exists before proceeding to classification
if os.path.exists("../data"):
    # 2- CLASSIFY WINES
    # Check for categorized files
    categorized_red_wines = os.path.join("../data", "red_wines_categorized.csv")
    categorized_white_wines = os.path.join("../data", "white_wines_categorized.csv")
    
    # Proceed only if both categorized files exist
    if os.path.exists(categorized_red_wines) and os.path.exists(categorized_white_wines):
        # Wine Clustering
        print("CLASSIFYING RED WINES")
        red, centroids_red = wcf.apply_clustering("../data", "red_wines_categorized.csv")

        print("CLASSIFYING WHITE WINES")
        white, centroids_white = wcf.apply_clustering("../data", "white_wines_categorized.csv")

        # Check for clustered data files
        red_clustered_file = os.path.join("../data", "red_wines_clustered.parquet")
        white_clustered_file = os.path.join("../data", "white_wines_clustered.parquet")

        # Ensure clustered files exist before proceeding
        if os.path.exists(red_clustered_file) and os.path.exists(white_clustered_file):
            # 3- CREATE USERS AND DISTRIBUTE WINES
            print("CREATING USERS AND CONFIGURING USERS' WINE DISTRIBUTION")
            user_list = uwdf.wine_delibery_conf("../data", "red_wines_clustered.parquet", "white_wines_clustered.parquet")
       
            # Save users data as JSON
            if user_list:  # Check if user_list is not empty
                uwdf.save_dict_list_json("../data", user_list)
            else:
                print("No users found for distribution configuration.")

print("SYSTEM DATABASE CORRECTLY CREATED.")
