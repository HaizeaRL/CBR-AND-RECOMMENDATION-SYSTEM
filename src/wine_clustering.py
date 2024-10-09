import os
import sys

# Add the parent directory (where modules is located) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# reference to functions 
from modules import wine_clustering_functions as wcf 

# APPLY CLUSTERING 
print("Applying clustering to RED wines...")
red, centroids_red = wcf.apply_clustering ("../data", "red_wines_categorized.csv")
print("Visualizing RED wines clustering...")
wcf.plot_clusters(red, centroids_red)
#
print("Applying clustering to WHITE wines...")
white, centroids_white = wcf.apply_clustering ("../data", "white_wines_categorized.csv")
print("Visualizing WHITE wines clustering...")
wcf.plot_clusters(white, centroids_white)
