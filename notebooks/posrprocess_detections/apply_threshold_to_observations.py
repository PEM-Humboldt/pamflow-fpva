"""
Processes detection files and filters based on species-specific confidence thresholds.

Parameters:
path_observations (str): Path to the directory containing detection CSV files.
path_save (str): Path to the directory where filtered CSV files will be saved.
species_th_path (str): Path to the CSV file containing species-specific confidence thresholds.

Returns: observations.csv filtered by species-specific thresholds and saves to output directory.
"""

import os
import pandas as pd


#%% Set variables
path_observations = '../../data/output/species_detection/unthresholded_observations.csv'
path_save = '../../data/output/species_detection/observations_updated.csv'
species_th_path = '../../data/output/species_detection/validation_based_thresholds.csv'

print("Loading species thresholds...")
# Load species thresholds
species_th = pd.read_csv(species_th_path)
species_th = species_th.set_index('scientificName')['proba_tpr0.95'].to_dict()
print("Species thresholds loaded.")

print("Loading detection files...")
# Load and merge detection files
df = pd.read_csv(path_observations)
print(f"Loaded {len(df)} observations.")

print("Processing detections based on species-specific thresholds...")
# Filter detections based on species-specific thresholds and save to output directory
observations_updated = pd.DataFrame()
for species, th in species_th.items():
    print(f"Filtering detections for species: {species} with threshold: {th}")
    df_sel = df.loc[(df['scientificName'] == species) & (df['classificationProbability'] >= th)]
    if df_sel.empty:
        print(f"No detections found for species {species} meeting the threshold {th}.")
    else:
        # add observations in df_sel to observations_updated
        observations_updated = pd.concat([observations_updated, df_sel], ignore_index=True)

print("Processing complete.")

# Manual revision
observations_updated.scientificName.value_counts()

# Save the updated observations
observations_updated.to_csv(path_save, index=False)
print(f"Filtered observations saved to {path_save}.")


