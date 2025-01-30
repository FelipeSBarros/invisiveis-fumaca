import logging

import geopandas as gpd


def filter_q90(
    gpkg_path="./Data/Processed/results.gpkg",
    territory="Localidades_Indigenas_pm2p5",
    variables=["media_temporada", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    q=0.9,
):
    logging.warning(f"Finding Quantile {q*100} for {territory} GeoDataFrame.")
    territory_gdf = gpd.read_file(gpkg_path, layer=territory)

    for variable in variables:
        if variable not in territory_gdf.columns:
            raise ValueError(f"{variable} not found in {territory} GeoDataFrame.")
        q90 = territory_gdf[variable].quantile(q)
        if q90 < 15:
            q90 = 15
        filtered_territory_gdf = territory_gdf[territory_gdf[variable] > q90]
        filtered_territory_gdf.to_file(
            gpkg_path, layer=f"{territory}_10%_afetadas_{variable}", driver="GPKG"
        )
        logging.warning(f"{territory}_10%_afetadas_{variable} saved in {gpkg_path}")


if __name__ == "__main__":
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Localidades_Indigenas_pm2p5",
        q=0.9,
    )
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Localidades_Quilombolas_pm2p5",
        q=0.9,
    )
    filter_q90(
        gpkg_path="./Data/Processed/results.gpkg",
        territory="Favelas_Comunidades_Urbanas_Centroide_pm2p5",
        q=0.9,
    )
