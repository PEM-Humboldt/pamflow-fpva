"""
Compute the Community Soundscape Similarity Index
Graphical soundscapes from sites are compared with two templates representing a dense forest and a grassland soundscape. The index is computed as the difference between the distance of the sample to the grassland template and the distance of the sample to the forest template. A positive index value indicates that the sample is more similar to the forest template, while a negative value indicates that it is more similar to the grassland template.
"""

import pandas as pd
from scipy.spatial.distance import pdist
import logging

# Set up logging
logger = logging.getLogger(__name__)

def compute_index(graph_partitioned_dataset, distance_metric, template_forest, template_grassland):
    """Compute the similarity index for each graph in the partitioned dataset."""

    index_values = pd.DataFrame(columns=['graphSimilarityIndex'])
    for graph_name, graph_load_func in sorted(graph_partitioned_dataset.items()):
        # load graphical soundscape sample data and format it as a 1D array
        sample = graph_load_func()
        sample = sample.values.ravel()
        deployment_id = graph_name.split("_")[1]  # extract deploymentID from graph name
        
        # compute distances to templates and calculate index value
        dist_forest = pdist([sample, template_forest["Forest"]], metric=distance_metric)
        dist_grassland = pdist([sample, template_grassland["Grassland"]], metric=distance_metric)
        index_value = dist_grassland[0] - dist_forest[0]
        
        # save index value for each graph in dataframe
        index_values.loc[deployment_id] = index_value
    
    # log that values were computed successfully
    logger.info("Graph similarity index values computed successfully.")
    index_values.reset_index(inplace=True)
    index_values.rename(columns={'index': 'deploymentID'}, inplace=True)
    
    return index_values
    
