"""
Compute the Community Soundscape Similarity Index
Graphical soundscapes from sites are compared with two templates representing a dense forest and a grassland soundscape. The index is computed as the difference between the distance of the sample to the grassland template and the distance of the sample to the forest template. A positive index value indicates that the sample is more similar to the forest template, while a negative value indicates that it is more similar to the grassland template.
"""

import pandas as pd
from scipy.spatial.distance import pdist

def validate_graph(path):
    sample = pd.read_csv(path)
    return pd.Series(sample.values.ravel())

def compute_index(sample, distance_metric, template_forest, template_grassland):
    dist_forest = pdist([sample, template_forest["Forest"]], metric=distance_metric)
    dist_grassland = pdist([sample, template_grassland["Grassland"]], metric=distance_metric)
    index_value = dist_grassland[0] - dist_forest[0]
    print(f"Index value: {index_value:.4f}")
    return index_value
    
