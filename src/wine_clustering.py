import os
import sys
import pandas as pd

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import wine_clustering_functions as wcf 

# APPLY CLUSTERING 
print("Applying clustering to RED wines...")
wcf.apply_clustering ("../files", "red_wines_categorized.csv")
#
print("Applying clustering to WHITE wines...")
wcf.apply_clustering ("../files", "white_wines_categorized.csv")

'''# SHOW RESULTS 
red = pd.read_parquet(os.path.join("../files","red_wines_clustered.parquet"),engine ="pyarrow")
print("RED")
print(red.head())
print(red["Zone"].value_counts())

white = pd.read_parquet(os.path.join("../files","white_wines_clustered.parquet"),engine ="pyarrow")
print("\nWHITE")
print(white.head())
print(white["Zone"].value_counts())'''