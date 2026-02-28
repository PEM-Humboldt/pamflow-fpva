""" Update observations csv using data from validations and based on custom species thresholds 

Akletos_melanoceps
Corythopis_torquatus
Crax_alector
Cyanocorax_violaceus
Formicarius_colma
Herpsilochmus_dorsimaculatus
Hylophylax_naevius
Liosceles_thoracicus
Lipaugus_vociferans
Myrmoborus_myotherinus
Myrmothera_campanisona
Nothocrax_urumutum
Percnostola_rufifrons
Phlegopsis_nigromaculata
Piaya_melanogaster
Ramphastos_tucanus
Thamnomanes_ardesiacus
Thamnomanes_caesius

"""
#%%
import pandas as pd

def load_validations(file_path):
    """Load data """
    data = pd.read_excel(file_path)
    # Transform 'no'/'yes' to 0/1 in 'positive' column. No case sensitivity.
    data['positive'] = data['positive'].str.lower().map({'no': 0, 'yes': 1})
    return data


# Variables
species = 'Thamnomanes_caesius'

# Load observations and validations
observations = pd.read_csv("../../data/output/species_detection/observations.csv")
validations = load_validations(f"../../data/output/species_detection/manual_annotations_validated/{species}_manual_annotations.xlsx")


#%% Step 1: Add observation ID to validations
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
    observations.loc[idx_obs, 'observationComments'] = row.observationComments

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
observations.loc[observations.observationID.isin(validations.observationID)]
observations.loc[observations.observationID.isin(validations.observationID)].scientificName.unique()
observations.classificationMethod.value_counts()

#%% Save
observations.to_csv("../../data/output/species_detection/observations.csv", index=False)
