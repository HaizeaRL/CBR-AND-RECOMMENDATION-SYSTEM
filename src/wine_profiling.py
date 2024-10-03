import os
import pandas as pd
import sys
pd.set_option("display.max_columns",None)

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import wine_profile_functions as wpf 

# CREATE WINE PROFILES & SAVE
wpf.wine_profiling("../files","red_wines.csv") # red wines
wpf.wine_profiling("../files","white_wines.csv") # white wines


'''# VALIDATE PROFILE CREATION 
red = pd.read_csv(os.path.join("../files","red_wines_categorized.csv"))
print(red)

VISUALIZING PROFILE
pos = 0
wpf.create_radar_plot(red.iloc[pos], title=f"Profile of Wine: #{pos+1}")'''
   