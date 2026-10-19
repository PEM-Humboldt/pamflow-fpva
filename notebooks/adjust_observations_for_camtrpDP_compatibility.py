""" 
Adjust observations.csv for compatibility with camtrapDP. 
- eventStart and eventEnd need to have dates formated as ISO8601 (YYYY-MM-DDTHH:MM:SSZ) and not as start and end of file.
- observationLevel needs to be set as "media"
- observationID is prefixed with the season code (e.g. 203 -> T3-203)
- frequencyLow and frequencyHigh are not camtrapDP fields and are dropped
"""

import pandas as pd

#%% User inputs
season_prefix = "T3"  # season code prepended to observationID

obs = pd.read_csv("../data/output_t3/species_detection/observations_updated.csv")
media = pd.read_csv("../data/output_t3/data_preparation/media.csv")[["mediaID", "timestamp"]]

#%% Adjust eventStart and eventEnd to be in ISO8601 format
# Merge media info to get timestamps
obs = obs.merge(media[["mediaID", "timestamp"]], on="mediaID", how="left")

# Convert eventStart and eventEnd to ISO8601 format using the timestamp
obs["timestamp"] = pd.to_datetime(obs["timestamp"])

# eventStart = timestamp + eventStart
obs["eventStart"] = obs["timestamp"] + pd.to_timedelta(obs["eventStart"], unit="s")

# eventEnd = timestamp + eventEnd
obs["eventEnd"] = obs["timestamp"] + pd.to_timedelta(obs["eventEnd"], unit="s")

# Format as ISO8601 with "T" separator and offset with colon (YYYY-MM-DDTHH:MM:SS-05:00)
for col in ["eventStart", "eventEnd"]:
    obs[col] = (obs[col].dt.strftime("%Y-%m-%dT%H:%M:%S%z")
                .str.replace(r"(\d{2})(\d{2})$", r"\1:\2", regex=True))

#%% Adjust observationLevel to "media"
obs["observationLevel"] = "media"

#%% Prefix observationID with the season code
obs["observationID"] = season_prefix + "-" + obs["observationID"].astype(str)

#%% Drop columns not in camtrapDP
obs = obs.drop(columns=["frequencyLow", "frequencyHigh"], errors="ignore")

#%% Save the adjusted observations
# drop the timestamp column as it's no longer needed
obs = obs.drop(columns=["timestamp"])
obs.to_csv("../data/output_t3/species_detection/observations_adjusted_I2D.csv", index=False)