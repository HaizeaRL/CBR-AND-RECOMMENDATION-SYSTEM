# wine clustering functions
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

def get_best_cluster_number (data):
    """
    Function that determines best cluster number calling to R script. 
    NbClust is applied to determine best cluster number by pooling.

    Parameters:
        data (dataframe): data to apply clustering.

    Returns:
        n_clusters: best cluster number       
    """  
    # Convert the scaled data back to a Pandas DataFrame for R interaction
    pandas2ri.activate() 

    # Load the R script and function 
    path = os.path.dirname(os.path.abspath(__file__))    
    ro.r['source'](os.path.join(path,"num_cluster_byNbclust_function.R"))
    num_cluster_by_NbClust = ro.globalenv['num_cluster_by_NbClust']

    # Call the R function with the appropriate arguments
    distance_method = ro.StrVector(["euclidean"])  # distance_method
    method = ro.StrVector(["kmeans"])              # method
    n_clusters = num_cluster_by_NbClust(data, distance_method, method)

    return n_clusters


def cluster_data (data, clustering_columns):
    """
    Function that applies clustering. Best cluster number determines calling to R script.

    Parameters:
        data (dataframe): data to apply clustering.
        clustering_columns (list(str)): list of columns to take into account in the clustering.

    Returns:
        n_clusters: best cluster number
        kmeans: kmeans model
        y_kmeans: clustering result
    """  

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data[clustering_columns])
    X_scaled_data = pd.DataFrame(X_scaled, columns= clustering_columns)

    # GET BEST CLUSTER NUMBER (by NbClust function in R script).  
    n_clusters = get_best_cluster_number(X_scaled_data) # get clusters only by clustering columns 

    # APPLY KMEANS
    kmeans = KMeans(n_clusters = int(n_clusters), init = 'k-means++', max_iter = 300, n_init = 10,
                    random_state = 0)
    y_kmeans = kmeans.fit_predict(X_scaled)

    return n_clusters, kmeans, y_kmeans


def character_list_by_clusters (n_clusters):
    """
    Function that generates a list of characters from A to the nth character

    Parameters:
        n_clusters (int): number that determines how many characters need to be created.

    Returns:
        value: return corresponding list of characters.
    """    

    return [f"Zone_{chr(i)}" for i in range(65, 65 + n_clusters)]

def create_map_dictionaries (n_clusters, kmeans, y_kmeans):
    """
    Function that generates map dictionaries.
    One relates cluster numbers with Zones. Example: cluster 0 = Zone A
    Other relates centroides with cluster numbeers. Example cluser 0 = Centroid data.

    Parameters:
        n_clusters : best cluster number
        kmeans: kmeans model
        y_kmeans: clustering result

    Returns:
        cluster_zone: map dictionary that relates cluster numbers with Zones.
        clusters_centroid:  map dictionary that relates cluster with its Centroid data.

    """   
    
    # Create cluster - zone map dictionary
    zones = character_list_by_clusters(int(n_clusters))
    clusters_zone = {i: zones[i] for i in set(y_kmeans)}

    # Create cluster - centroid relation map dsctionary
    centroids = kmeans.cluster_centers_
    # save as np.array not as string
    clusters_centroid = {i: centroids[i] for i in set(y_kmeans)}

    return clusters_zone, clusters_centroid


def apply_clustering (path, filename):
    """
    Function that applies clustering to corresponding data.
    Scales, determine best cluster number, clusters and add new columns with resulted values.

    Parameters:
        path (str): path to files.
        filename (str): filename to load and apply clustering

    Returns:
        Null
        But saves clustered data with "_clustered.csv" name
    """   

    # LOAD DATA 
    filename_root = filename.split("_categorized.csv")[0]
    df = pd.read_csv(os.path.join(path, filename))

    # APPLY CLUSTERING
    clustering_cols = ['residual sugar', 'chlorides', 'sulphates', 'Body_tmp', 'Vibrancy_tmp']
    n_clusters, kmeans, y_kmeans = cluster_data(df , clustering_cols)

    # DETERMINE EACH WINES ZONE (based on clusters)
    clusters_zone, clusters_centroid = create_map_dictionaries (n_clusters, kmeans, y_kmeans)

    # ADD NEW COLUMNS
    df.loc[:,"Cluster"] = y_kmeans
    df.loc[:,"Centroid"] = df["Cluster"].map(clusters_centroid)
    df.loc[:,"Zone"] = df["Cluster"].map(clusters_zone)

    # save clustered data
    new_filename = f"{filename_root}_clustered.parquet"
    df.to_parquet(os.path.join(path,new_filename), engine ="pyarrow")