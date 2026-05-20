from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    calculate_birds_index,
    remove_failed_deployments_birds_index,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(  # Log
                func=calculate_birds_index,
                inputs=[
                    "thresholds@pandas",
                    "observations@pamDP",
                ],
                outputs="birds_index_raw",
                name="birds_index_node",
            ),
            node(
                func=remove_failed_deployments_birds_index,
                inputs=[
                    "birds_index_raw",
                    "deployments@pamDP"],
                outputs="birds_index@pandas",
                name="remove_failed_deployments_birds_index_node",
            ),

        ]
    )
