# Graph Similarity Index Pipeline

This pipeline computes a community soundscape similarity index for each deployment by comparing sample graphical soundscapes against forest and grassland templates.

## Purpose

The `graph_similarity_index` pipeline quantifies how similar each deployment's graphical soundscape is to a forest template versus a grassland template. Positive values indicate forest-like similarity, while negative values indicate grassland-like similarity.

## Input datasets

- `graphical_soundscape@PartitionedDataset`: partitioned graphs sampled from deployment soundscapes.
- `params:graph_similarity_index.distance`: the distance metric used to compare soundscape features.
- `template_forest@pandas`: forest template vector used as a reference.
- `template_grassland@pandas`: grassland template vector used as a reference.

## Output dataset

- `graph_similarity_index@pandas`: a CSV dataset containing one similarity index value per `deploymentID`.

## What it does

1. Iterates over each partitioned graphical soundscape sample.
2. Loads the sample and flattens it into a feature vector.
3. Computes the distance from the sample to the forest template.
4. Computes the distance from the sample to the grassland template.
5. Calculates the index as `distance_to_grassland - distance_to_forest`.
6. Saves the computed index for each deployment.

## Where results are stored

The output dataset is configured in `conf/base/catalog/graph_similarity_index.yml` and writes to:

`data/output/similarity_index/graph_similarity_index.csv`

## Pipeline usage

This pipeline is registered as `graph_similarity_index` in `src/pamflow/pipeline_registry.py` and can be run as part of the Kedro workflow.

Example:

```bash
kedro run --pipeline graph_similarity_index
```
