# import library
library(NbClust)

# Disable any graphical output
options(bitmapType='cairo')
pdf(NULL)

# function that determine best cluster number
num_cluster_by_NbClust <- function(data, distance_method, method){
  
  # Apply NbClust to data 
  set.seed(42)  
  nbclust_results <- NbClust(data, 
                             diss = NULL, 
                             distance = distance_method,
                             min.nc = 2, 
                             max.nc = 20, 
                             method = method)  
  
  # get summary and best cluster numbers
  bests <- as.data.frame(nbclust_results$Best.nc)
  #print(bests)
  
  # transpose and get only cluster numbers
  n_clusters = as.data.frame(t(bests))["Number_clusters"]
  
  # obtain max frequency value and indexes of those values from n_clusters
  freq_table = table(n_clusters)
  max_indexes = as.numeric(names(freq_table[freq_table == max(freq_table)]))
  
  # if many indexes get the last
  return (max_indexes[length(max_indexes)])
}
