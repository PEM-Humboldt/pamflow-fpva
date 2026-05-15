""" Update observations csv using data from validations and based on custom species thresholds 

"""
#%%
import pandas as pd
import os

def load_validations(file_path):
    """Load data """
    data = pd.read_excel(file_path)
    # remove NaN rows which where not validated
    data = data.dropna(subset=['positive'])
    if data.dtypes['positive'] == 'object':
        # Transform 'no'/'yes' to 0/1 in 'positive' column. No case sensitivity.
        data['positive'] = data['positive'].str.lower().map({'TRUE': 0, 'FALSE': 1})
    return data

# Variables
observations = pd.read_csv("../../data/output_t2/species_detection/observations.csv")
species_list = pd.read_csv('../../data/input/target_species/target_species.csv').scientificName.tolist()
path_annotations = "../../data/output_t2/species_detection/manual_annotations/"

#%%
for species in species_list:
    species = species.replace(' ', '_')
    # Load Validations
    try:
        file_path = os.path.join(path_annotations, f"{species}_manual_annotations.xlsx")
        validations = load_validations(file_path)
    except FileNotFoundError:
        print(f"File not found for species: {species}")
        continue
    
    #% Add observation ID to validations
    for idx, row in validations.iterrows():
        # get observation index
        idx_obs = observations.observationID==row.observationID
        # update classificationMethod to human
        observations.loc[idx_obs, 'classificationMethod'] = 'human'
        # update classifiedBy
        observations.loc[idx_obs, 'classifiedBy'] = row.classifiedBy
        # update classificationTimestamp Formatted as an ISO 8601 string with timezone designator as today. To hour accuracy maximum.
        observations.loc[idx_obs, 'classificationTimestamp'] = pd.Timestamp.now(tz='America/Bogota').strftime('%Y-%m-%dT%H:%M:%S%z')
        # update observationComments
        observations.loc[idx_obs, 'observationComments'] = row.observationsComments

        if row.positive == 1:
            # scientific name is unchanged
            # update classificationProbability
            observations.loc[idx_obs, 'classificationProbability'] = 1.0
        
        elif row.positive == 0:
            # Set scientificName as empty
            observations.loc[idx_obs, 'scientificName'] = row.detectedSpecies
            # update classificationProbability
            observations.loc[idx_obs, 'classificationProbability'] = 1.0
        
        elif pd.isna(row.positive):
            # Set scientificName as empty
            observations.loc[idx_obs, 'scientificName'] = 'Aves'
            # update classificationProbability
            observations.loc[idx_obs, 'classificationProbability'] = 1.0

        else:
            print(f'Unknown value: {row.positive}')
    
    
#%% Revise
observations.classifiedBy.value_counts()
observations.loc[observations.classificationMethod=='human'].scientificName.value_counts()

#%% Save
#observations.to_csv("../../data/output_t2/species_detection/unthresholded_observations.csv", index=False)
