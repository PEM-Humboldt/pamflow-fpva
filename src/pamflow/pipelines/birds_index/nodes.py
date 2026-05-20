import pandas as pd
import numpy as np
import logging

# Set up logging
logger = logging.getLogger(__name__)


def calculate_birds_index(df_thresholds: pd.DataFrame, df_observations: pd.DataFrame) -> pd.DataFrame:
    """
    Filters bird observations based on quality thresholds and calculates 
    a normalized diversity index per deployment.
    """
    # 1. Filter for valid thresholds
    valid_thresholds = df_thresholds[df_thresholds['Comments'] == 'ok']
    total_unique_species = valid_thresholds['scientificName'].nunique()
    
    if total_unique_species == 0:
        raise ValueError("No valid species found in thresholds after filtering 'Comments' == 'ok'.")

    # 2. Filter and merge observations with thresholds
    filtered_obs = df_observations[df_observations['scientificName'].isin(valid_thresholds['scientificName'])]
    merged_df = filtered_obs.merge(valid_thresholds, on='scientificName', how='left')

    # 3. Identify confident detections (true positive rate at 95% confidence)
    is_confident_detection = merged_df['classificationProbability'] >= merged_df['proba_tpr0.95']
    merged_df['confident_species'] = np.where(is_confident_detection, merged_df['scientificName'], None)

    # 4. Aggregate by deployment and normalize the index
    birds_index_df = (
        merged_df
        .groupby('deploymentID')
        .agg(unique_confident_birds=('confident_species', 'nunique'))
        .reset_index()
    )
    
    birds_index_df['indice'] = birds_index_df['unique_confident_birds'] / total_unique_species
    
    return birds_index_df[['deploymentID', 'indice']]

def remove_failed_deployments_birds_index(birds_index, deployments):
    """ Replace invalid index values by NaN for deployments that had quality issues """
    col = 'deploymentTags'
    
    if col not in deployments.columns or deployments[col].isna().all() or (deployments[col] == '').all():
        logger.warning("No deployment quality information found in 'deploymentTags' — values left unchanged.")
        return birds_index
    
    failed_deployments = deployments.deploymentID[
        deployments[col] == 'deploymentQuality:failed'
    ].tolist()
    
    if not failed_deployments:
        logger.info("No failed deployments found — values left unchanged.")
        return birds_index
    
    birds_index.loc[
        birds_index['deploymentID'].isin(failed_deployments), 
        'indice'
    ] = np.nan
    
    logger.info(f"Invalid birds index removed for {len(failed_deployments)} failed deployment(s).")
    return birds_index
