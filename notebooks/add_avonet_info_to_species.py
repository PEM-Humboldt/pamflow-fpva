""" Add traits from AVONET to species dataframe """

import pandas as pd

trait_cols = ["Species2", "Habitat", "Habitat.Density", "Trophic.Level", "Trophic.Niche"]
df_species = pd.read_csv("../data/output/species_detection/observations_per_species.csv")
df_avonet = pd.read_excel("../data/input/AVONET/AVONET_dataset.xlsx", sheet_name="AVONET2_eBird")[trait_cols]

df_out = pd.merge(df_species, df_avonet, how="left", left_on="scientificName", right_on="Species2")

df_out.to_csv("../data/output/species_detection/observations_per_species_with_avonet_info.csv", index=False)

