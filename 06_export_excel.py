import logging
import re

import geopandas as gpd
import pandas as pd


def export_excel(
    gpkg_path="./Data/Processed/results.gpkg",
    variables=["media_temporada", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
):
    logging.warning(f"Exporting {variables} GeoDataFrame to Excel.")
    layers_list = gpd.list_layers(gpkg_path)
    for variable in variables:
        logging.warning(f"Starting with {variable}.")
        # variable = variables[0]
        layers = layers_list[
            layers_list["name"].str.contains(
                f"{variable}*", na=False, flags=re.IGNORECASE
            )
        ]
        layers_gdf = gpd.GeoDataFrame(
            pd.concat(
                [gpd.read_file(gpkg_path, layer=layer) for layer in layers.name],
                ignore_index=True,
            )
        )
        layers_gdf.drop("geometry", axis=1, inplace=True)
        layers_gdf.to_excel(f"./Data/Processed/resultado_{variable}.xlsx")
        logging.warning(f"Export completed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    export_excel(
        gpkg_path="./Data/Processed/results.gpkg",
        variables=["media_temporada", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    )
    setores = gpd.read_file(
        "./Data/Processed/results.gpkg", layer="Setores_Censitarios_2022_pm2p5"
    )
    setores.drop("geometry", axis=1, inplace=True)
    setores.to_excel(f"./Data/Processed/resultado_setores.xlsx")
    tis = gpd.read_file("./Data/Processed/results.gpkg", layer="TerrasIndigenas_2022_pm2p5")
    tis.drop("geometry", axis=1, inplace=True)
    tis.to_excel(f"./Data/Processed/resultado_tis.xlsx")
