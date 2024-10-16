import os
import pandas as pd
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import user_profile_functions as upf
from modules import wine_recommendation_functions as wrf

# RECOMMEND WINES BASED ON USERS PROFILE
print("Please specify who you are from the list below:\n")
user_list = upf.get_user_list("../data", "users_wine_delivery_conf.json")
print(' | '.join(f"User: '{x}'" for x in upf.get_users_references(user_list)))
user_id = input("You are? ")
print(f"\nHello '{user_id}'!")
print("Based on your wine profile, I will provide you new wine recommendations. Please hold on a moment... \n")

# Get users data
user_data, user_red_cat, user_white_cat =  upf.get_specific_user_info (user_list, user_id)
   
# Get recommendation data
distribution, solution_red, solution_white = wrf.recommend_wines(user_data, user_red_cat, user_white_cat)
recommendation_text = wrf.create_recommendation_text (distribution, solution_red, solution_white)

# Complete recommendation pdf
output_file = upf.create_recomendation_pdf(user_data, user_red_cat, user_white_cat , user_id, 
                                           solution_red, solution_white, recommendation_text)

print(f"Recomendation file create. Please check in {output_file}")