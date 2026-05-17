"""
This is a boilerplate pipeline 'graph_similarity_index'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, node
from .nodes import compute_index, remove_failed_deployments


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
                outputs="graph_similarity_index_raw",
                name="compute_similarity_index_node",
            ),
            node(
                func=remove_failed_deployments,
                inputs=[
                    "graph_similarity_index_raw",
                    "deployments@pamDP"],
                outputs="graph_similarity_index@pandas",
                name="remove_failed_deployments_node",
            ),
        ])
