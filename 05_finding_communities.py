import geopandas as gpd


def filter_q90(
    gpkg_path="./Data/Processed/results.gpkg",
    territory="Localidades_Indigenas_pm2p5",
    variable="media_temporada",
    q=0.9,
):
    territory_gdf = gpd.read_file(gpkg_path, layer=territory)

    q90 = territory_gdf[variable].quantile(q)
    territory_gdf = territory_gdf[territory_gdf[variable] > q90]
    territory_gdf.to_file(gpkg_path, layer=f"{territory}_10%_afetadas", driver="GPKG")
    return


if __name__ == "__main__":
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Localidades_Indigenas_pm2p5",
        variable="media_temporada",
        q=0.9,
    )
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Localidades_Quilombolas_pm2p5",
        variable="media_temporada",
        q=0.9,
    )
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Favelas_Comunidades_Urbanas_Centroide_pm2p5",
        variable="media_temporada",
        q=0.9,
    )
