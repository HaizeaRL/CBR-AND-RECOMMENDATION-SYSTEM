# wine clustering functions
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import itertools 
import matplotlib.pyplot as plt
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

# global variable
clustering_cols = ['residual sugar', 'chlorides', 'sulphates', 'Body_tmp', 'Vibrancy_tmp']

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


def cluster_data (data):
    """
    Function that applies clustering. Best cluster number determines calling to R script.

    Parameters:
        data (dataframe): data to apply clustering.

    Returns:
        n_clusters: best cluster number
        kmeans: kmeans model
        y_kmeans: clustering result
    """  

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data[clustering_cols])
    X_scaled_data = pd.DataFrame(X_scaled, columns= clustering_cols)

    # GET BEST CLUSTER NUMBER (by NbClust function in R script).  
    n_clusters = get_best_cluster_number(X_scaled_data) # get clusters only by clustering columns 

    # APPLY KMEANS
    kmeans = KMeans(n_clusters = int(n_clusters), init = 'k-means++', max_iter = 300, n_init = 10,
                    random_state = 0)
    y_kmeans = kmeans.fit_predict(X_scaled)

    return X_scaled, n_clusters, kmeans, y_kmeans


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
        centroids: centroids summary

    """   
    
    # Create cluster - zone map dictionary
    zones = character_list_by_clusters(int(n_clusters))
    clusters_zone = {i: zones[i] for i in set(y_kmeans)}

    # Create cluster - centroid relation map dsctionary
    centroids = kmeans.cluster_centers_

    # save as np.array not as string
    clusters_centroid = {i: centroids[i] for i in set(y_kmeans)}

    return clusters_zone, clusters_centroid, centroids


def apply_clustering (path, filename):
    """
    Function that applies clustering to corresponding data.
    Scales, determine best cluster number, clusters and add new columns with resulted values.

    Parameters:
        path (str): path to data.
        filename (str): filename to load and apply clustering

    Returns:
        Null
        But saves clustered data with "_clustered.csv" name
    """   

    # LOAD DATA 
    filename_root = filename.split("_categorized.csv")[0]
    df = pd.read_csv(os.path.join(path, filename))

    # APPLY CLUSTERING 
    X_scaled, n_clusters, kmeans, y_kmeans = cluster_data(df)

    # DETERMINE EACH WINES ZONE (based on clusters)
    clusters_zone, clusters_centroid, centroids= create_map_dictionaries (n_clusters, kmeans, y_kmeans)

    # add scaled data to origin df
    X_scaled_data = pd.DataFrame(X_scaled, columns=clustering_cols)
    X_scaled_data = X_scaled_data.add_suffix('_scaled')
    df_combined = pd.concat([df, X_scaled_data], axis=1)

    # ADD NEW columns 
    df_combined.loc[:,"Cluster"] = y_kmeans
    df_combined.loc[:,"Centroid"] = df_combined["Cluster"].map(clusters_centroid)
    df_combined.loc[:,"Zone"] = df_combined["Cluster"].map(clusters_zone)

    # save clustered data in correct formats
    new_filename = f"{filename_root}_clustered.parquet"
    df_combined.to_parquet(os.path.join(path,new_filename), engine ="pyarrow")

    return df_combined, centroids

def plot_clusters(data, centroids):

    """
    Function that plots clusters and its centroids.

    Parameters:
        data (dataframe): dataframe to filter to plot clusters
        centroids (np.array): centroids values per cluster.
    Returns:
        Null
    """   
    # Pair combinations of columns for plotting
    new_cols = [x +"_scaled" for x in clustering_cols]
    cols_combination = list(itertools.combinations(new_cols, 2))

    # Map 'Zone' column to unique colors
    zones = data['Zone'].unique()  # Get unique zones
    color_map = {zone: color for zone, color in zip(zones, plt.cm.get_cmap('viridis', len(zones)).colors)}

    for combination in cols_combination:
        plt.figure(figsize=(12, 6))
        
        # plot data points, diferentiate clusters or zones by colors
        plt.scatter(data[combination[0]], data[combination[1]], 
                    c=data['Zone'].map(color_map), alpha=0.6)
        
        # Scatter plot for centroids
        plt.scatter(centroids[:, new_cols.index(combination[0])], 
                    centroids[:, new_cols.index(combination[1])], 
                    c='red', marker='x', label='Centroids')  # Red X for centroids

        # create the legend manually: data points + centroids
        legend_handler = [plt.Line2D([0], [0], marker='o', color=color_map[zone], linestyle='None', 
                              markersize=10, label=f'{zone}') for zone in zones]
        legend_handler.append(plt.Line2D([0], [0], marker='x', color='red', markersize=8, label='Centroids'))
        
        # add legend
        plt.legend(handles=legend_handler, title="Legend")

        # set title and axis labels
        plt.xlabel(combination[0])
        plt.ylabel(combination[1])
        plt.title(f'Scatter plot of {combination[0]} vs {combination[1]} with centroids')

        # adjust and show plot
        plt.tight_layout()
        plt.show()