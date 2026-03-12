"""
This is a boilerplate pipeline 'graph_similarity_index'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, node
from .nodes import compute_index, validate_graph


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=validate_graph,
                inputs="params:graph_similarity_index.sample_graph_path",
                outputs="graph_sample@pandas",
                name="validate_graph_node",
            ),
            node(
                func=compute_index,
                inputs=[
                    "graph_sample@pandas", 
                    "params:graph_similarity_index.distance", 
                    "template_forest@pandas", 
                    "template_grassland@pandas"],
                outputs="similarity_index_value@float",
                name="compute_similarity_index_node",
            ),
        ])
