import os
import concurrent.futures
import pandas as pd
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import logging
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