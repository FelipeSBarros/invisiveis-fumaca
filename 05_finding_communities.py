import geopandas as gpd
import folium

amz_setores = gpd.read_file(
    "./Data/Processed/results.gpkg", layer="Setores_Censitarios_2022_pm2p5"
)
amz_setores = gpd.read_file(
    "./Data/Processed/results.gpkg", layer="setores_top_50_pm2p5_albers"
)
#
# # Identifica e filtra os 50 setores censitários com maiores valores de pm2p5
top_50 = amz_setores.nlargest(500, "media_temporada")
# top_50.to_file("./Data/Processed/results.gpkg", driver="GPKG", layer='setores_top_50_pm2p5')
# # converte o SRC a projetado, realiza um buffer de 2 km e converte de volta ao SRC geográfico
amz_setores_buffer = amz_setores.buffer(2000).to_crs(4326).to_frame()
# amz_setores_buffer.to_file("./Data/Processed/results.gpkg", driver="GPKG", layer='setores_top_50_pm2p5_buffer')
loc_indigenas = gpd.read_file(
    "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg", layer="Lodalidades_Indigenas"
)
loc_indigenas.shape
filtered_points = gpd.sjoin(loc_indigenas, amz_setores_buffer, predicate="within")
filtered_points = filtered_points[loc_indigenas.columns]  # Keep only original point columns

loc_indigenas.shape
loc_quilombola = geopandas.read_file(
    "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg", layer="Localidades_Quilombolas"
)

favelas = geopandas.read_file(
    "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg", layer="Favelas_Comunidades_Urbanas"
)

