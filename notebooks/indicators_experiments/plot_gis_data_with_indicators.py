""" Integrate GIS data into the indicators computed """

#%% -- LOAD LIBRARIES AND FUNCTIONS -- 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% -- SECTION 1. PLOT GIS PERCENT of COVER as REGPLOT--
# Load data
#df_graph_t1 = pd.read_csv("../../data/output_t1/similarity_index/graph_similarity_index.csv")
#df_graph_t2 = pd.read_csv("../../data/output_t2/similarity_index/graph_similarity_index.csv")
df_graph_t1 = pd.read_csv("../../data/output_t1/birds_index/avifauna_interior_bosque.csv")
df_graph_t2 = pd.read_csv("../../data/output_t2/birds_index/avifauna_interior_bosque.csv")
index_col = "indice"  # "graphSimilarityIndex" or "indice" for birds index
df_gis = pd.read_csv("../../data/input/field_deployments/location_gis_categories_percent.csv")[["locationID", "Bosques"]]
df_deployments_t1 = pd.read_csv("../../data/output_t1/data_preparation/deployments.csv")[["deploymentID", "locationID"]]
df_deployments_t2 = pd.read_csv("../../data/output_t2/data_preparation/deployments.csv")[["deploymentID", "locationID"]]

# Merge results with deployments to get locationID for GIS data
df_graph_t1_ = df_graph_t1.merge(df_deployments_t1, on="deploymentID", how="left")
df_graph_t2_ = df_graph_t2.merge(df_deployments_t2, on="deploymentID", how="left")

# Merge GIS data with indicators
df_graph_t1_gis = df_graph_t1_.merge(df_gis, on="locationID", how="left")
df_graph_t2_gis = df_graph_t2_.merge(df_gis, on="locationID", how="left")

#%% Plotting
# Graph similarity index by cobertura
fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)

sns.regplot(data=df_graph_t1_gis, x="Bosques", y=index_col, ax=axes[0],
            scatter_kws={"color": "tab:blue"}, line_kws={"color": "tab:blue"})
axes[0].set_title("T1")

sns.regplot(data=df_graph_t2_gis, x="Bosques", y=index_col, ax=axes[1],
            scatter_kws={"color": "tab:orange"}, line_kws={"color": "tab:orange"})
axes[1].set_title("T2")
axes[1].set_ylabel("")  # avoid duplicate y label

# Dotted line at y=0 for reference
for ax in axes:
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)

# Set x and y label
axes[0].set_ylabel("Índice de Avifauna")
axes[0].set_xlabel("Cobertura de Bosque (%)")
axes[1].set_xlabel("Cobertura de Bosque (%)")

# enforce same ranges explicitly
#ymin = min(-0.43, -0.43)
#ymax = max(0.43, 0.43)
ymin = min(0, 0)
ymax = max(1, 1)

xmin = min(df_graph_t1_gis["Bosques"].min(), df_graph_t2_gis["Bosques"].min())
xmax = max(df_graph_t1_gis["Bosques"].max(), df_graph_t2_gis["Bosques"].max())

for ax in axes:
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(xmin, xmax)

plt.tight_layout()
sns.despine(trim=True)
plt.tight_layout()
plt.savefig("./figures/indiceAvifauna__bosques_percent_regplot.png", dpi=300)


#%% -- SECTION 3. PLOT CHANGES BETWEEN SEASONS --
# Plot 1: Difference in index values in each location between seasons as barplot
# Plot 2: Boxplot overlay with swarmplot for categorical variable, faceted by season

# Load data for both seasons
#df_graph_t1 = pd.read_csv("../../data/output_t1/similarity_index/graph_similarity_index.csv")
#df_graph_t2 = pd.read_csv("../../data/output_t2/similarity_index/graph_similarity_index.csv")
df_graph_t1 = pd.read_csv("../../data/output_t1/birds_index/avifauna_interior_bosque.csv")
df_graph_t2 = pd.read_csv("../../data/output_t2/birds_index/avifauna_interior_bosque.csv")
index_col = "indice"  # "graphSimilarityIndex" or "indice" for birds index
df_gis = pd.read_csv("../../data/input/field_deployments/location_gis_categories_percent.csv")[["locationID", "Bosque_prop"]]
df_deployments_t1 = pd.read_csv("../../data/output_t1/data_preparation/deployments.csv")[["deploymentID", "locationID"]]
df_deployments_t2 = pd.read_csv("../../data/output_t2/data_preparation/deployments.csv")[["deploymentID", "locationID"]]

# Merge results with deployments to get locationID for GIS data
df_graph_t1['season'] = 'T1'
df_graph_t2['season'] = 'T2'
df_graph = pd.concat([
    df_graph_t1.merge(df_deployments_t1, on="deploymentID", how="left"),
    df_graph_t2.merge(df_deployments_t2, on="deploymentID", how="left")
], ignore_index=True)
df_graph_gis = df_graph.merge(df_gis, on="locationID", how="left")

#%% Plotting
# -- Difference in index values in each location between seasons as lolliplot
# each x value is a location, y value is the index difference, and the color is the category 'cobertura'.
df_graph_diff = df_graph_gis.pivot_table(index="locationID", columns="season", values=index_col).reset_index()
df_graph_diff["difference"] = df_graph_diff["T2"] - df_graph_diff["T1"]
df_graph_diff = df_graph_diff.merge(df_gis[["locationID", "Bosque_prop"]], on="locationID", how="left")

# final adjustments for plotting
df_graph_diff.sort_values("difference", inplace=True)  # Sort by difference for better visualization
df_graph_diff.dropna(subset=["difference"], inplace=True)  # Drop rows with NaN differences

# Adjust legend to have more descriptive labels
df_graph_diff["Bosque_prop"] = df_graph_diff["Bosque_prop"].map({
    "baja": "Baja (0-33%)",
    "media": "Media (34-66%)",
    "alta": "Alta (67-100%)"
})
df_graph_diff.rename(columns={"Bosque_prop": "Cobertura de Bosque"}, inplace=True)
# save the plot
sns.barplot(data=df_graph_diff, x="difference", y="locationID", hue="Cobertura de Bosque", palette="Set2")
plt.xlabel("Diferencia en Índice (T2 - T1)")
plt.ylabel("ID de Ubicación")
sns.despine(left=True, trim=True)
plt.tight_layout()
plt.savefig(f"./figures/{index_col}_seasonal_differences_barplot.png", dpi=300)

# -- Boxplot overlay with swarmplot for categorical variable, faceted by season

g = sns.catplot(
    data=df_graph_gis, 
    x="Bosque_prop", 
    y=index_col, 
    hue="season",
    order=["baja", "media", "alta"], 
    palette="Set2", 
    kind="box",
    height=5,
    aspect=1.2,
)

g.set_axis_labels("Cobertura de Bosque", "Índice de avifauna de interior de bosque")
g.set_xticklabels(["Baja (0-33%)", "Media (34-66%)", "Alta (67-100%)"])
sns.despine(trim=True)
#plt.tight_layout()
plt.savefig(f"./figures/{index_col}_seasonal_differences_boxplot.png", dpi=300)
