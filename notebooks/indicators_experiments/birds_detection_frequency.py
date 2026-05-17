import pandas as pd

# Load data
observations = pd.read_csv("../../data/output_t1/species_detection/observations.csv")
media = pd.read_csv("../../data/output_t1/data_preparation/media.csv")[["mediaID", "deploymentID", "timestamp"]]

# Target species
target_species = [
    "Akletos melanoceps",
    "Myrmoborus myotherinus",
    "Myrmothera campanisona",
    "Cyanocorax violaceus",
    "Hylophylax naevius",
    #"Ramphastos tucanus",
    "Thamnomanes ardesiacus",
    #"Lipaugus vociferans",
    "Thamnomanes caesius"
]

# Filter target species and merge
obs = (
    observations
    .query("scientificName in @target_species")
    .drop(columns=["deploymentID"])
    .merge(media, on="mediaID", how="left")
)

# Parse dates
obs["date"] = pd.to_datetime(obs["timestamp"]).dt.date
media["date"] = pd.to_datetime(media["timestamp"]).dt.date

# Total recording days per deployment (from media, not observations)
recording_days = (
    media
    .drop_duplicates(subset=["deploymentID", "date"])
    .groupby("deploymentID")["date"]
    .nunique()
    .reset_index(name="total_days")
)

# Detection days per deployment x species (unique days only)
detection_days = (
    obs
    .drop_duplicates(subset=["deploymentID", "scientificName", "date"])
    .groupby(["deploymentID", "scientificName"])["date"]
    .nunique()
    .reset_index(name="detected_days")
)

# Full grid: all combinations of deployment x species
deployments = media["deploymentID"].unique()
grid = pd.MultiIndex.from_product(
    [deployments, target_species],
    names=["deploymentID", "scientificName"]
).to_frame(index=False)

# Merge grid with detections and recording effort, fill absences with 0
detection_freq = (
    grid
    .merge(detection_days, on=["deploymentID", "scientificName"], how="left")
    .merge(recording_days, on="deploymentID", how="left")
    .fillna({"detected_days": 0})
    .assign(frequency=lambda x: x["detected_days"] / x["total_days"])
)

# Indicator per deployment (mean frequency across species)
indicator_by_site = (
    detection_freq
    .groupby("deploymentID")["frequency"]
    .mean()
    .reset_index(name="indicator")
    .sort_values("indicator", ascending=False)
)

# Regional indicator (mean frequency across species and deployments)
regional_indicator = detection_freq["frequency"].mean()

print(indicator_by_site)
print(f"\nRegional indicator: {regional_indicator:.3f}")

# Compare with other indicator
df = pd.read_csv("../../data/output_t1/similarity_index/graph_similarity_index.csv")
df = df.merge(indicator_by_site, on="deploymentID", how="left")

import seaborn as sns
sns.regplot(data=df, x='graphSimilarityIndex', y='indicator', scatter=True, color='red')

import statsmodels.api as sm
# 3. Regresión Lineal Detallada
X = sm.add_constant(df['graphSimilarityIndex']) # añade intercepto
model = sm.OLS(df['indicator'], X).fit()
model.summary()