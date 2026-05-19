import os
import concurrent.futures
import pandas as pd
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import logging

# Set up logging
logger = logging.getLogger(__name__)


from pamflow.pipelines.species_detection.utils import (
    species_detection_single_file,
    trim_audio,
)
from pamflow.datasets.pamDP.observations import observations_pamdp_columns
from rich.console import Console

def birds_index(thresholds, observations):
    #tpr_conf01,proba_tpr0.95
    thresholds=thresholds[thresholds['Comments']=='ok']

    observations = observations[observations['scientificName'].isin(thresholds['scientificName'])]
    observations = observations.merge(thresholds, 
                                    on='scientificName', 
                                    how='left'
                                    )

    birds_index=observations.assign(#conf01= np.where(observations['classificationProbability']>=observations['tpr_conf01'], 
                                                    #observations['scientificName'], 
                                                    #None
                                                    #),
                    conf095= np.where(observations['classificationProbability']>=observations['proba_tpr0.95'],
                                                    observations['scientificName'],
                                                    None
                                                    )
                                
                    ).groupby('deploymentID').agg(#indice_01=('conf01', 'nunique'), 
                                                    indice=('conf095', 'nunique')
                                                    ).reset_index()

    birds_index['indice'] = birds_index['indice']/thresholds['scientificName'].nunique()
    return birds_index

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
