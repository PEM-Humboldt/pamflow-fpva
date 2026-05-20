""" 
Adjust observations.csv for compatibility with camtrapDP. 
- eventStart and eventEnd need to have dates formated as ISO8601 (YYYY-MM-DDTHH:MM:SSZ) and not as start and end of file.
- observationLevel needs to be set as "media"
"""

import pandas as pd

obs = pd.read_csv("../../data/output_t2/species_detection/observations.csv")
media = pd.read_csv("../../data/output_t2/data_preparation/media.csv")[["mediaID", "timestamp"]]

#%% Adjust eventStart and eventEnd to be in ISO8601 format
# Merge media info to get timestamps
obs = obs.merge(media[["mediaID", "timestamp"]], on="mediaID", how="left")

# Convert eventStart and eventEnd to ISO8601 format using the timestamp
obs["timestamp"] = pd.to_datetime(obs["timestamp"])

# eventStart = timestamp + eventStart
obs["eventStart"] = obs["timestamp"] + pd.to_timedelta(obs["eventStart"], unit="s")

# eventEnd = timestamp + eventEnd
obs["eventEnd"] = obs["timestamp"] + pd.to_timedelta(obs["eventEnd"], unit="s")

#%% Adjust observationLevel to "media"
obs["observationLevel"] = "media"

#%% Save the adjusted observations
# drop the timestamp column as it's no longer needed
obs = obs.drop(columns=["timestamp"])
obs.to_csv("../../data/output_t2/species_detection/observations_adjusted_I2D.csv", index=False)