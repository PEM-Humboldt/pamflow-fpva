import pandas as pd

df = pd.read_csv('../data/output_t2/species_detection/observations.csv')

mask = df['classificationTimestamp'].str.contains(r'[-+]\d{4}$', na=False, regex=True)
print(f"Rows with timezone offset: {len(df[mask])}")

df['classificationTimestamp'] = pd.to_datetime(
    df['classificationTimestamp'], 
    format='ISO8601',
    utc=True
).dt.strftime('%Y-%m-%dT%H:%M:%S')

df.to_csv('../data/output_t2/species_detection/observations_clean.csv', index=False)
print(f"Done. All timestamps normalized to ISO8601 without offset.")
