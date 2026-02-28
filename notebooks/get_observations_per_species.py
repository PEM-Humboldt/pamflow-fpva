""" Get observations per species from annotations """

import pandas as pd

obs = pd.read_csv("../data/output/species_detection/unfiltered_observations.csv")

df_out = obs["scientificName"].value_counts()

# remove species that have less than 30 observations
df_out = df_out[df_out >= 30]

df_out.to_csv("../data/output/species_detection/observations_per_species.csv")