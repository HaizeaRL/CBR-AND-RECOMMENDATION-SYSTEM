import os 
import pandas as pd
import json
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import user_wine_distribution_functions as uwdf 


# create users and its wine delivery configuration.
user_list = uwdf.wine_delibery_conf("../data", "red_wines_clustered", "white_wines_clustered")
# save data as json
if len(user_list) > 0:
    uwdf.save_dict_list_json("../data", user_list)    
    print("Users wine delivery created and saved.")    
    

  
