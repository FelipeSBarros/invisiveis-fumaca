# Importando bibliotecas necessárias
import xvec
import logging
import geopandas as gpd
import xarray as xr

# Carregando o dataset XArray com os dados de PM2.5
ds = xr.open_dataset("./Data/Processed/CAMS_AMZ_combined.nc")

# Calculando a média de PM2.5 para toda a temporada
# A função `groupby` organiza os dados por ano e `mean` calcula a média.
season_mean = ds.groupby("Brasilia_reference_time.year").mean()

# Calculando a média mensal do PM2.5 e salvando o resultado
monthly_mean = ds.groupby("Brasilia_reference_time.month").mean()


def extract_values(gpkg_path, territory_layer_name, output_path):
    territory = gpd.read_file(gpkg_path, layer=territory_layer_name)
    # Calculando estatísticas zonais para todo o período
    # Calculando estatísticas zonais mensais
    logging.warning(f"Extracting pm2p5 monthly mean values for {territory_layer_name}.")
    monthly_stats = monthly_mean.xvec.zonal_stats(
        territory.geometry,
        x_coords="longitude",
        y_coords="latitude",
        method="exactextract",
    )

    logging.warning(f"Extracting pm2p5 season mean values for {territory_layer_name}.")
    season_stats = season_mean.xvec.zonal_stats(
        territory.geometry,
        x_coords="longitude",
        y_coords="latitude",
        method="exactextract",
    )

    # Convertendo os resultados das estatísticas zonais para um GeoDataFrame
    logging.warning(
        f"Converting and organizing results to GeoDataFrame for {territory_layer_name}."
    )
    monthly_stats_df = monthly_stats.xvec.to_geodataframe(name="pm2p5").reset_index()
    season_stats_df = season_stats.xvec.to_geodataframe(name="pm2p5").reset_index()

    # Adicionando um ID único para cada município por mês
    monthly_stats_df["id"] = monthly_stats_df.groupby("month").cumcount()

    # Removendo a coluna de geometria, já que não será usada na transformação para formato "wide"
    monthly_stats_df = monthly_stats_df.drop(columns=["geometry"])
    season_stats_df = season_stats_df.drop(columns=["geometry"])

    # Transformando o DataFrame para formato "wide" (colunas por mês)
    monthly_stats_df = monthly_stats_df.pivot(
        columns="month", index="id", values="pm2p5"
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

    # Fazendo o join com os limites dos municípios
    # A opção `inner` garante que apenas os municípios com dados sejam mantidos.
    logging.warning(f"Joining results with {territory_layer_name} boundaries.")
    monthly_gdf = territory.join(monthly_stats_df, how="inner")
    final_gdf = monthly_gdf.join(season_stats_df, how="inner")

    # Exibindo o DataFrame final para verificar os resultados
    logging.warning(f"Saving GeoDataFrame in {output_path}")
    final_gdf.to_file(output_path, layer=f"{territory_layer_name}_pm2p5", driver="GPKG")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Municipios_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="Setores_Censitarios_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    extract_values(
        gpkg_path="./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg",
        territory_layer_name="TerrasIndigenas_2022",
        output_path="./Data/Processed/results.gpkg",
    )
    logging.warning("Extração de valores concluída com sucesso!")
