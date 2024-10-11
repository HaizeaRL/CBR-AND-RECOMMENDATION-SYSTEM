import os
import pandas as pd
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import wine_profile_functions as wpf 

# CREATE WINE PROFILES & SAVE
print("CREATING WINE PROFILE")
wpf.wine_profiling("../data","red_wines.csv") # red wines
wpf.wine_profiling("../data","white_wines.csv") # white wines


# reference to functions 
from modules import wine_clustering_functions as wcf 

# CLASSIFY WINES
print("CLASSIFYING RED WINES")
red, centroids_red = wcf.apply_clustering ("../data", "red_wines_categorized.csv")
print("\nCLASSIFYING WHITE WINES")
white, centroids_red = wcf.apply_clustering ("../data", "white_wines_categorized.csv")

# reference to functions 
from modules import user_wine_distribution_functions as uwdf 

# CREATE USERS AND DISTRIBUTE WINES PER USERS
print("CREATING USERS AND CONFIGURING USERS WINE DISTRIBUTION")
user_list = uwdf.wine_delibery_conf("../data", "red_wines_clustered", "white_wines_clustered")
# save users data as json
if len(user_list) > 0:
    uwdf.save_dict_list_json("../data", user_list)    
    print("Users wine delivery created and saved.")    
    

print("SYSTEM DATABASE CORRECTLY CREATED.")