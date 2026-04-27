from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    birds_index
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(  # Log
                func=birds_index,
                inputs=[
                    "thresholds@pandas",
                    "observations@pamDP",
                ],
                outputs="birds_index@pandas",
                name="birds_index_node",
            ),
            
        ]
    )
