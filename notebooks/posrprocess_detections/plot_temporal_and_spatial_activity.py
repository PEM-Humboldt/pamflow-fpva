""" Plot spatial and temporal activity of species detections. 

"""

#%% Load libraries
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


#%% Set variables
path_observations = '../../data/output/species_detection/observations.csv'
path_deployments = '../../data/output/data_preparation/deployments.csv'
path_media = '../../data/output/data_preparation/media.csv'

# Load observations
observations = pd.read_csv(path_observations)
deployments = pd.read_csv(path_deployments)
media = pd.read_csv(path_media)

# add deployment location to observations by merging on deploymentID
observations = observations.merge(deployments[['deploymentID', 'latitude', 'longitude']], on='deploymentID', how='left')

# add media timestamp to observations by merging on mediaID
observations = observations.merge(media[['mediaID', 'timestamp']], on='mediaID', how='left')
#observations.to_csv('figures/vocal_activity/observations_with_location_and_time.csv', index=False)

#%% Filter observations for the focal species
species_list = observations['scientificName'].unique()
species_list = species_list[species_list != 'Phlegopsis nigromaculata']  # Remove this species because it has only 1 detection and it is an outlier in the temporal activity pattern

for species in species_list:
    
    # Filter observations for the focal species
    obs_focal_species = observations.loc[observations['scientificName'] == species]

    #%% 1. Plot spatial activity using geopandas and contextily

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        obs_focal_species, geometry=gpd.points_from_xy(obs_focal_species.longitude, obs_focal_species.latitude),
        crs="EPSG:4326"
    )

    fig, ax = plt.subplots(figsize=(10, 10))
    gdf = gdf.to_crs(epsg=3857)  # Web Mercator for contextily

    # Count detections per location
    detection_counts = gdf.groupby('deploymentID').size()
    detection_counts = detection_counts / media.deploymentID.value_counts()[detection_counts.index] * 48 # Normalize by number of media per deployment
    gdf['detection_count'] = gdf['deploymentID'].map(detection_counts)

    # Plot all deployments (including zero detections)
    all_deployments_gdf = gpd.GeoDataFrame(
        deployments, geometry=gpd.points_from_xy(deployments.longitude, deployments.latitude),
        crs="EPSG:4326"
    ).to_crs(epsg=3857)
    all_deployments_gdf['detection_count'] = all_deployments_gdf['deploymentID'].map(detection_counts).fillna(0)

    # Plot zero detections in light gray
    zero_detections = all_deployments_gdf[all_deployments_gdf['detection_count'] == 0]
    zero_detections.plot(ax=ax, color='gray', alpha=0.6, markersize=15)

    # Make cmap from blues starting from blue to darkblue
    colors = ['lightblue', 'blue', 'darkblue']
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)


    # Plot detections with color and size based on count
    gdf.plot(
        ax=ax, 
        column='detection_count', 
        cmap=cmap, 
        alpha=0.3, 
        markersize=gdf['detection_count'] / gdf['detection_count'].max() * 500, 
        legend=True
        )
    
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)

    # Enlarge map vertically by adjusting y-axis limits
    current_ylim = ax.get_ylim()
    y_range = current_ylim[1] - current_ylim[0]
    ax.set_ylim(current_ylim[0] - y_range * 0.25, current_ylim[1] + y_range * 0.25)

    ax.text(0.97, 0.97, species, 
            transform=ax.transAxes, ha='right', va='top', style='italic', fontsize=11)
    ax.text(0.97, 0.93, f'N={len(obs_focal_species)} detecciones',
            transform=ax.transAxes, ha='right', va='top', fontsize=10)
    ax.set_title(f'Patrón de actividad espacial')
    plt.show()
    plt.savefig(f'figures/vocal_activity/spatial_activity_{species}.pdf', dpi=300)
    plt.close()

    #%% 2. Plot temporal activity
    obs_focal_species['timestamp'] = pd.to_datetime(obs_focal_species['timestamp'])
    obs_focal_species['hour'] = obs_focal_species['timestamp'].dt.hour

    # plot histogram with kde 1D overlayed plot goes from 0 to 23 hours
    plt.figure(figsize=(8, 6))
    plt.hist(obs_focal_species['hour'], bins=24, range=(0, 24), alpha=0.4, color='darkblue', density=True)
    obs_focal_species['hour'].plot.kde(color='darkblue', linewidth=2)
    # add text with species name at top right corner
    plt.text(0.97, 0.97, species, transform=plt.gca().transAxes, ha='right', va='top', style='italic', fontsize=11)
    plt.title(f'Patrón de actividad vocal temporal')
    plt.xlabel('Hora del día')
    plt.ylabel('Densidad')
    plt.savefig(f'figures/vocal_activity/temporal_activity_{species}.pdf', dpi=300)
    plt.close()