# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:00:29 2024
Get similarity wines
@author: hrumayor
"""

import os
import pandas as pd
import numpy as np

pd.set_option("display.max.columns",None)

df = pd.read_parquet(os.path.join("C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/files",
                              "red_wines_clustered.parquet"), engine = "pyarrow")



# Step 2: Define a function to calculate Euclidean distance between two centroids
def euclidean_distance(centroid1, centroid2):
    return np.linalg.norm(centroid1 - centroid2)

# Function to calculate Manhattan distance
def manhattan_distance(vec1, vec2):
    return np.sum(np.abs(vec1 - vec2))

# Function to calculate Cosine similarity
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Select the row of interest 
selected_row = df.loc[445]
cols = list(df.columns)


# Compute distances between the selected row's Centroid and all other rows' Centroids
df['Euclidean_Distance'] = df['Centroid'].apply(lambda x: euclidean_distance(selected_row['Centroid'], x))
df['Manhattan_Distance'] = df['Centroid'].apply(lambda x: manhattan_distance(selected_row['Centroid'], x))
df['Cosine_Similarity_Distance'] = df['Centroid'].apply(lambda x: cosine_similarity(selected_row['Centroid'], x))

# Find the row with the minimum distance (excluding the selected row itself)
nearest_row = df[df.index != selected_row.name].loc[df['Euclidean_Distance'].idxmin()]
nearest_row_manhattan = df[df.index != selected_row.name].loc[df['Manhattan_Distance'].idxmin()]
nearest_row_cosine = df[df.index != selected_row.name].loc[df['Cosine_Similarity_Distance'].idxmax()]

# Convert the dictionaries to pandas Series
to_remove = ['Euclidean_Distance','Manhattan_Distance','Cosine_Similarity_Distance',"Cluster","Centroid"]
a = [cols for cols in df.columns if cols not in to_remove]

selected_series = pd.Series(selected_row[a])
nearest_series = pd.Series(nearest_row[a])
nearest_manhattan_s = pd.Series(nearest_row_manhattan[a])
nearest_cosine_s = pd.Series(nearest_row_cosine[a])

selected_row

# Create the DataFrame
solution = pd.DataFrame({
    "Attribute": selected_series.index,
    "Selected": selected_series.values,
    "Nearest_euclidean": nearest_series.values,
    "Nearest_manhatan": nearest_manhattan_s.values,
    "Nearest_cosine": nearest_cosine_s.values,
    
})


print(solution)

# TODO: use one distance function depending on parameter
# TODO: visualize centroid, selected row data and nearest data
# TODO: visualize information in interesting form
