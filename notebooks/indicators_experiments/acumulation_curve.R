library(vegan)
library(tidyverse)

# Select species
especies_objetivo <- c(
  "Akletos melanoceps",
  "Myrmoborus myotherinus",
  "Myrmothera campanisona",
  "Cyanocorax violaceus",
  "Hylophylax naevius",
  "Ramphastos tucanus",
  "Thamnomanes ardesiacus",
  "Lipaugus vociferans",
  "Thamnomanes caesius"
)

# Load observations
obs <- read.csv("data/output_t2/species_detection/observations.csv") %>%
  filter(scientificName %in% especies_objetivo)
media <- read_csv("data/output_t2/data_preparation/media.csv") %>%
  select(mediaID, timestamp)



obs_merged <- obs %>%
  left_join(media, by = "mediaID")

mat <- obs_merged %>%
  mutate(dia = as.Date(timestamp)) %>%
  distinct(dia, scientificName, deploymentID) %>%  # una detección por especie-día-sitio
  mutate(presente = 1) %>%
  pivot_wider(
    id_cols = scientificName,
    names_from = c(deploymentID, dia),
    values_from = presente,
    values_fill = 0
  ) %>%
  column_to_rownames("scientificName") %>%
  as.matrix()

# specaccum hace rarefacción por permutaciones
# matriz sitios x especies (transpuesta)
acc <- specaccum(t(mat), method = "random", permutations = 100)

# extraer los valores de la curva
df_acc <- data.frame(
  sites = acc$sites,
  richness = acc$richness
)

# calcular la pendiente entre unidades consecutivas
df_acc <- df_acc %>%
  mutate(pendiente = c(NA, diff(richness) / diff(sites)))

# ver dónde la pendiente cae por debajo de un umbral
umbral <- 0.01  # menos de 0.01 especies por unidad adicional

df_acc %>% filter(pendiente < umbral) %>% slice(1)

# punto de inflexión
punto <- df_acc %>% filter(pendiente < umbral) %>% slice(1)
plot(acc)
abline(v = punto$sites, col = "red", lty = 2)
text(x = punto$sites + 5,
     y = min(acc$richness),
     labels = paste0("n = ", round(punto$sites), "\nS = ", round(punto$richness, 1)),
     col = "red", adj = 0, cex = 0.85)