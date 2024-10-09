import os
import pandas as pd
import sys
pd.set_option("display.max_columns",None)

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import wine_profile_functions as wpf 

# CREATE WINE PROFILES & SAVE
wpf.wine_profiling("../data","red_wines.csv") # red wines
wpf.wine_profiling("../data","white_wines.csv") # white wines


# VALIDATE PROFILE CREATION 
red = pd.read_csv(os.path.join("../data","red_wines_categorized.csv"))
white = pd.read_csv(os.path.join("../data","white_wines_categorized.csv"))

# VISUALIZING PROFILE
pos = 444
wpf.create_radar_plot(red.iloc[pos], title=f"RED: Profile of Wine: #{pos+1}")
wpf.create_radar_plot(white.iloc[pos], title=f"WHITE: Profile of Wine: #{pos+1}")