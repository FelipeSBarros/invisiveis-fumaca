# Importando bibliotecas necessárias
import logging
import xvec
from pathlib import Path

import geopandas as gpd
import xarray as xr

from testes import focos

# Carregando o dataset xarray com os dados médios de PM2.5 para toda a temporada
season_mean = xr.open_dataset("./Data/Processed/season_mean_pm2p5.nc")

# Carregando o dataset xarray com os dados médios mensais de PM2.5
monthly_mean = xr.open_dataset("./Data/Processed/monthly_mean_pm2p5.nc")

max_values = xr.open_dataset(
    "./Data/Processed/max_values_pm2p5.nc", decode_coords="all"
)

# Carregando dado de focos de calor
focos = gpd.read_file(
    "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
    layer="Focos_NPP375_tarde",
)


def extract_values(gpkg_path, territory_layer_name, output_path, zonal_stats=True):
    if not Path(gpkg_path).exists():
        raise FileNotFoundError(f"File {gpkg_path} not found.")

    territory = gpd.read_file(gpkg_path, layer=territory_layer_name)
    if not zonal_stats:
        # sample the monthly_mean DataSet according to territory point location
        logging.warning(
            f"Extracting pm2p5 monthly mean values for {territory_layer_name}."
        )
        monthly_stats = monthly_mean.xvec.extract_points(
            territory.geometry, x_coords="longitude", y_coords="latitude"
        )
        # Calculando estatísticas zonais para todo o período
        logging.warning(
            f"Extracting pm2p5 season mean values for {territory_layer_name}."
        )
        season_stats = season_mean.xvec.extract_points(
            territory.geometry, x_coords="longitude", y_coords="latitude"
        )
        max_stats_val = max_values.xvec.extract_points(
            territory.geometry,
            x_coords="longitude",
            y_coords="latitude",
        )

    if zonal_stats:
        # Calculando estatísticas zonais mensais
        logging.warning(
            f"Extracting pm2p5 monthly mean values for {territory_layer_name}."
        )
        monthly_stats = monthly_mean.xvec.zonal_stats(
            territory.geometry,
            x_coords="longitude",
            y_coords="latitude",
            method="exactextract",
        )
        # Calculando estatísticas zonais para todo o período
        logging.warning(
            f"Extracting pm2p5 season mean values for {territory_layer_name}."
        )
        season_stats = season_mean.xvec.zonal_stats(
            territory.geometry,
            x_coords="longitude",
            y_coords="latitude",
            method="exactextract",
        )
        max_stats_val = max_values.xvec.zonal_stats(
            territory.geometry,
            x_coords="longitude",
            y_coords="latitude",
            stats=["max"],
            method="exactextract",
        )

        # Perform spatial join to find points within polygons
        joined = gpd.sjoin(focos, territory, predicate="within")
        total_focos = (
            joined.groupby(["index_right"])
            .size()
            .to_frame("total_focos")
        )
        territory = territory.merge(
            total_focos, left_index=True, right_index=True, how="left"
        )
        # Count points within each polygon using the polygon's unique ID
        point_counts = (
            joined.groupby(["index_right", "mes"])
            .size()
            .to_frame("total_mes")
            .reset_index(drop=False)
        )
        # convert DataFrame to wide format setting mes as columns and total_mes as values
        point_counts = point_counts.pivot(
            index="index_right", columns="mes", values="total_mes"
        )
        point_counts = point_counts.rename(
            columns={
                col: f"focos_mes_{col}"
                for col in point_counts.columns
                if 7 <= col <= 12
            },
        )
        # point_counts.reset_index(drop=True, inplace=True)
        # join the joined DataFrame with point_counts by the index_right column
        territory = territory.merge(
            point_counts, left_index=True, right_index=True, how="left"
        )
        # territory.to_file("Data/Processed/results.gpkg", layer="GPKG")

    # Convertendo os resultados das estatísticas zonais para um GeoDataFrame
    logging.warning(
        f"Converting and organizing results to GeoDataFrame for {territory_layer_name}."
    )
    monthly_stats_df = monthly_stats.xvec.to_geodataframe(name="pm2p5").reset_index()
    season_stats_df = season_stats.xvec.to_geodataframe(name="pm2p5").reset_index()
    max_stats_df = max_stats_val.xvec.to_geodataframe(name="vallue").reset_index()

    # Adicionando um ID único para cada município por mês
    monthly_stats_df["id"] = monthly_stats_df.groupby("month").cumcount()

    # Removendo a coluna de geometria, já que não será usada na transformação para formato "wide"
    monthly_stats_df = monthly_stats_df.drop(columns=["geometry"])
    # Transformando o DataFrame para formato "wide" (colunas por mês)
    monthly_stats_df = monthly_stats_df.pivot(
        columns="month", index="id", values="pm2p5"
    )
    season_stats_df = season_stats_df.drop(columns=["geometry"])
    # Pivot para reorganizar os dados em formato wide
    if not "max_month" in list(max_stats_df.columns):
        max_stats_df = max_stats_df.pivot_table(
            index=max_stats_df.groupby("variable").cumcount(),
            columns="variable",
            values="value",
            aggfunc="first",
        )

    season_stats_df = season_stats_df.pivot(columns="year", values="pm2p5")
    season_stats_df.columns = ["media_temporada"]

    # Renomeando as colunas para os meses correspondentes
    monthly_stats_df.columns = [
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
    ]

    # Fazendo o join com o limite territorial
    logging.warning(f"Joining results with {territory_layer_name} boundaries.")
    monthly_gdf = territory.join(monthly_stats_df, how="inner")
    monthly_gdf = monthly_gdf.join(max_stats_df[["max_value", "max_month"]], how="inner")
    final_gdf = monthly_gdf.join(season_stats_df, how="inner")

    # Salvando o GeoDataFrame em um arquivo GeoPackage
    logging.warning(f"Saving GeoDataFrame in {output_path}")
    final_gdf.to_file(output_path, layer=f"{territory_layer_name}_pm2p5", driver="GPKG")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Localidades_Quilombolas",
        output_path="./Data/Processed/results.gpkg",
        zonal_stats=False,
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Localidades_Indigenas",
        output_path="./Data/Processed/results.gpkg",
        zonal_stats=False,
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Favelas_Comunidades_Urbanas_Centroide",
        output_path="./Data/Processed/results.gpkg",
        zonal_stats=False,
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Municipios_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="TerrasIndigenas_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Setores_Censitarios_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    logging.warning("Extração de valores concluída com sucesso!")
