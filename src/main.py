import os
import pandas as pd
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import user_profile_functions as upf


# RECOMMEND WINES BASED ON USERS PROFILE
print("Please specify who you are from the list below:\n")
user_list = upf.get_user_list("../data", "users_wine_delivery_conf.json")
print(' | '.join(f"User: '{x}'" for x in upf.get_users_references(user_list)))
user_id = input("You are? ")
print(f"\nHello '{user_id}'!")
print("Based on your wine profile, I will provide you new wine recommendations. Please hold on a moment... \n")
output_file = upf.create_recomendation_pdf(user_list, user_id)
print(f"Recomendation file create. Please check in {output_file}")