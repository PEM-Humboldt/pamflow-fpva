Explannation to execute the postprocessing

1. Compute detections with birdnet using pamflow

2. Validate segments with different confidence values

3. Get threshold for 95% TP rate, species by species
`python find_birdnet_threshold.py -i <input_csv>`

4. Add manual validations to observations table
Run script species by species: `add_manual_validation_to_observations.py`

4. Postprocess detections according to thresholds
Run step by step: `apply_threshold to observations`