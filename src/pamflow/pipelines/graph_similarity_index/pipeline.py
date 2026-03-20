"""
This is a boilerplate pipeline 'graph_similarity_index'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, node
from .nodes import compute_index


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=compute_index,
                inputs=[
                    "graphical_soundscape@PartitionedDataset", 
                    "params:graph_similarity_index.distance", 
                    "template_forest@pandas", 
                    "template_grassland@pandas"],
                outputs="graph_similarity_index@pandas",
                name="compute_similarity_index_node",
            ),
        ])
