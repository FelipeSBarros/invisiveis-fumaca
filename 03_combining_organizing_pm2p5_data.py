import logging  # Para registrar logs de execução
import rioxarray # para trabalhar com xarray e rasterio
from glob import glob  # Importa glob para buscar arquivos no sistema
from pathlib import Path  # Para manipulação de caminhos de arquivos

import geopandas as gpd
import numpy as np  # Importa numpy para operações numéricas
import pandas as pd  # Importa pandas para manipulação de datas e tempos
import xarray as xr  # Importa o xarray para trabalhar com datasets multidimensionais


def identify_critical_pixels(
    ds,
    n_critical_pixels=20,
    output_file="top_critical_pixels_mask",
):
    logging.warning(f"Criando máscara de píxels críticos: {output_file}")
    # Selecionar a variável de interesse
    if isinstance(ds, xr.Dataset):
        pm2p5 = ds["pm2p5"]
    else:
        pm2p5 = ds
    # Obter valores válidos (ignorar NaN)
    valid_values = pm2p5.values[~np.isnan(pm2p5.values)]

    # Determinar o limite do menor valor entre os n maiores
    threshold_value = np.partition(valid_values, -n_critical_pixels)[-n_critical_pixels]

    # Criar uma máscara binária: 1 para valores maiores/iguais ao limite, 0 para os demais
    mask = xr.where(pm2p5 >= threshold_value, 1, 0)

    # Configurar atributos geoespaciais
    mask = mask.rio.write_nodata(0)
    mask = mask.rio.write_crs(pm2p5.rio.crs)
    mask = mask.rio.write_transform(pm2p5.rio.transform())

    # Garantir a ordem de dimensões para compatibilidade com exportação
    if len(mask.dims) == 3:
        mask = mask.transpose(list(mask.dims)[0], "latitude", "longitude")
    else:
        mask = mask.transpose("latitude", "longitude")

    # Exportar a máscara como GeoTIFF
    mask.rio.to_raster(f"{output_file}.tif", dtype="uint8")

    logging.warning(f"Máscara salva em: {output_file}")

    # data = rioxarray.open_rasterio(f"{output_file}.tif", mask_and_scale=True).squeeze()
    # data.name = output_file
    # gdf = vectorize(data)
    # gdf.to_file(
    #     f"./Data/Processed/results.gpkg",
    #     driver="GPKG",
    #     layer=output_file.split("/")[-1],
    # )
    # logging.warning(f"{output_file} vetorizado")


def combine_datasets():
    # 1. Obtenha a lista de arquivos NetCDF presentes em um diretório e subdiretórios.
    datasets = glob("./Data/Raw/CAMS_AMZ/unzipped/*/*.nc")
    if not datasets:
        logging.warning("No datasets found to process.")
        return

    logging.warning(f"Found {len(datasets)} datasets to process.")
    # Carregar o limite da Amazonia Legal
    gpkg_path = "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg"
    if not gpkg_path:
        logging.warning(
            "Geopakcgae not found. Please donwload it from https://drive.google.com/file/d/17XwGFL5njDCzJGRp_T0i_Imn5n-PBscE/view?usp=sharing and save into ./Data/Raw/IBGE/"
        )
        return

    legal_amz = gpd.read_file(
        gpkg_path,
        layer="Municipios_2022",
    )

    # 2. Crie uma lista para armazenar os datasets processados
    processed_datasets = []

    # 3. Itere sobre cada arquivo NetCDF para carregar e processar os dados
    for file in datasets:
        logging.warning(f"Processing {file}: converting to UTC-3 and combining times.")
        ds = xr.open_dataset(file)  # Carrega o dataset do arquivo NetCDF

        # 4. Converter a variável 'forecast_reference_time' para pandas datetime
        # A 'forecast_reference_time' indica o momento de referência da previsão.
        forecast_reference_time_pandas = pd.to_datetime(
            ds["forecast_reference_time"].values
        )

        # 5. Converter a variável 'forecast_period' para timedelta
        # 'forecast_period' é o tempo relativo da previsão, que é em horas. Vamos convertê-lo para o formato timedelta.
        forecast_period_timedelta = pd.to_timedelta(
            ds["forecast_period"].values, unit="h"
        )

        # 6. Garantir que ambas as variáveis sejam numpy arrays para facilitar as operações numéricas
        forecast_reference_time_numpy = forecast_reference_time_pandas.values
        forecast_period_numpy = forecast_period_timedelta.values

        # 7. Expandir as dimensões das variáveis para permitir broadcasting durante a operação de soma
        # 'forecast_reference_time' será expandida na segunda dimensão (coluna), e 'forecast_period' será expandida na primeira dimensão (linha)
        forecast_reference_time_expanded = np.expand_dims(
            forecast_reference_time_numpy, axis=1
        )  # Forma (N, 1)
        forecast_period_expanded = np.expand_dims(
            forecast_period_numpy, axis=0
        )  # Forma (1, M)

        # 8. Combinar as duas variáveis expandidas (referência temporal e período de previsão) para obter os tempos combinados
        combined_times = forecast_reference_time_expanded + forecast_period_expanded

        # 9. Converter os tempos combinados para pandas datetime e ajustar para o fuso horário de Brasília
        # Primeiramente, convertemos definimos o fuso horário (UTC), para depois converter ao horário de Brasília.
        combined_times_flat = (
            pd.to_datetime(
                combined_times.ravel()
            )  # Flattening para transformar em uma única lista
            .tz_localize("UTC")  # Localiza no fuso horário UTC
            .tz_convert("America/Sao_Paulo")  # Converte para o horário de Brasília
            .tz_localize(None)  # Remove a informação de fuso horário
        )

        # 10. Criar uma coordenada unidimensional para 'Brasilia_reference_time'
        combined_times_1d = (
            combined_times_flat.to_numpy()
        )  # Converte para numpy array unidimensional

        # 12. Colapsar as dimensões 'forecast_reference_time' e 'forecast_period' em uma nova dimensão 'flat_time'
        # Isso cria uma única dimensão combinando as duas dimensões anteriores, simplificando o acesso aos dados
        ds = ds.stack({"flat_time": ("forecast_reference_time", "forecast_period")})

        # 13. Adicionar a nova coordenada 'Brasilia_reference_time' associada à nova dimensão 'flat_time'
        ds = ds.assign_coords(
            {"Brasilia_reference_time": ("flat_time", combined_times_1d)}
        )

        # 14. Substituir a dimensão antiga 'flat_time' pela nova dimensão 'Brasilia_reference_time'
        ds = ds.swap_dims({"flat_time": "Brasilia_reference_time"})

        # 15. Remover as dimensões e variáveis antigas que não são mais necessárias
        # A remoção inclui as variáveis 'forecast_reference_time', 'forecast_period', 'valid_time', e 'flat_time'
        ds = ds.drop_vars(
            ["forecast_reference_time", "forecast_period", "valid_time", "flat_time"]
        )

        # 16. Transpor as dimensões para que 'longitude' e 'latitude' sejam as primeiras dimensões
        ds = ds.transpose("longitude", "latitude", "Brasilia_reference_time")
        ds = ds.rio.write_crs("EPSG:4326")

        # 16. Adicionar o dataset processado à lista de datasets
        logging.warning(f"Processed dataset")
        processed_datasets.append(ds)

    # 17. Concatenar todos os datasets processados ao longo da nova dimensão 'Brasilia_reference_time'
    logging.warning("Concatenating datasets.")
    ds = xr.concat(processed_datasets, dim="Brasilia_reference_time")
    ds.Brasilia_reference_time.attrs["timezone"] = "America/Sao_Paulo"
    # limita os dados até o mes de dezembro de 2024
    ds = ds.where(
        (
            ds["Brasilia_reference_time"]
            >= np.datetime64("2024-07-01T00:00:00.000000000")
        )
        & (
            ds["Brasilia_reference_time"]
            <= np.datetime64("2024-12-31T23:59:59.999999999")
        ),
        drop=True,
    )
    # 18. Converter os valores de 'pm2p5' de unidades para 'ug/m³'
    logging.warning("Converting pm2p5 units.")
    ds["pm2p5"] = (
        ds["pm2p5"] * 1e9
    )  # Multiplica por 1 bilhão (10^9) para converter para microgramas

    # 19. Atualizar os atributos do dataset para refletir as novas unidades
    ds.attrs["units"] = "ug/m3"

    # 20. Recortar o dataset para a Amazônia Legal
    logging.warning("clipping to Legal Amazon Territory.")
    ds = ds.rio.clip(legal_amz.geometry, legal_amz.crs, drop=True)

    # 21. Salvar o dataset final em um novo arquivo NetCDF
    logging.warning("Saving combined dataset.")
    ds.to_netcdf("./Data/Processed/CAMS_AMZ_combined.nc")
    # crop ds to legal_amz GeoDataFrame

    # 22. Calculando a média de PM2.5 para toda a temporada
    # A função `groupby` organiza os dados por ano e `mean` calcula a média.
    if not Path("./Data/Processed/season_mean_pm2p5.nc").exists():
        logging.warning("Calculating season mean.")
        season_mean = ds.groupby("Brasilia_reference_time.year").mean()
        season_mean.to_netcdf("./Data/Processed/season_mean_pm2p5.nc")
        logging.warning("Exporting monthly mean to tif.")
        season_mean = season_mean.pm2p5.transpose("year", "latitude", "longitude")
        season_mean.rio.to_raster("./Data/Processed/season_mean_pm2p5.tif")
        # Calcula mascara de pixels críticos
        identify_critical_pixels(
            ds=season_mean,
            n_critical_pixels=20,
            output_file="./Data/Processed/season_mean_20_top_critical_pixels_mask",
        )

    # 23. Calculando a média mensal do PM2.5 e salvando o resultado
    if not Path("./Data/Processed/monthly_mean_pm2p5.nc").exists():
        logging.warning("Calculating monthly mean.")
        monthly_mean = ds.groupby("Brasilia_reference_time.month").mean()
        for month in monthly_mean["month"].values:
            subset = monthly_mean.sel(month=month)
            identify_critical_pixels(
                ds=subset,
                n_critical_pixels=20,
                output_file=f"./Data/Processed/month_{month}_pm2p5_20_top_critical_pixels_mask",
            )
        monthly_mean = monthly_mean.pm2p5.transpose("month", "latitude", "longitude")
        monthly_mean.to_netcdf("./Data/Processed/monthly_mean_pm2p5.nc")
        logging.warning("Exporting monthly mean to tif.")
        monthly_mean.rio.to_raster("./Data/Processed/monthly_mean_pm2p5.tif")

    # 24. Calculando a mediana para todo o periodo
    if not Path("./Data/Processed/median_pm2p5.tif").exists():
        logging.warning("Calculating median.")
        median = ds.pm2p5.median(dim="Brasilia_reference_time")
        identify_critical_pixels(
            ds=median,
            n_critical_pixels=20,
            output_file="./Data/Processed/median_pm2p5_20_top_critical_pixels_mask",
        )
        # median.to_netcdf("./Data/Processed/median_pm2p5.nc")
        logging.warning("Exporting median to tif.")
        median = median.transpose("latitude", "longitude")
        median.rio.to_raster("./Data/Processed/median_pm2p5.tif")

    # 25. Calculando a quantidade de dias acima de 15 ug/m³
    if not Path("./Data/Processed/days_above_15.tif").exists():
        logging.warning("Calculating days above 15 ug/m³.")
        # sum the amount of days that the value of pm2p5 was over 15
        days_above_15 = ds.groupby("Brasilia_reference_time.date").mean().pm2p5 > 15
        days_above_15 = days_above_15.sum(dim="date", skipna=True)
        days_above_15 = days_above_15.transpose("latitude", "longitude")
        days_above_15 = days_above_15.rio.write_crs("EPSG:4326")
        days_above_15 = days_above_15.astype("int32")
        # days_above_15 = xr.where(ds['pm2p5'].isnull().all(dim="Brasilia_reference_time"), float("nan"), days_above_15)
        # days_above_15.to_netcdf("./Data/Processed/days_above_15.nc")
        logging.warning("Exporting days above 15 to tif.")
        days_above_15.rio.to_raster("./Data/Processed/days_above_15.tif")
        identify_critical_pixels(
            ds=days_above_15,
            n_critical_pixels=20,
            output_file="./Data/Processed/days_above_15_pm2p5_20_top_critical_pixels_mask",
        )

    # 26. Calculando o valor maximo diario de pm2p5 para todo o periodo
    if not Path("./Data/Processed/max_pm2p5.tif").exists():
        logging.warning("Calculating max pm2p5.")
        daily_mean = ds.groupby("Brasilia_reference_time.date").mean()

        # Identificar o valor máximo de pm2p5 ao longo do tempo
        max_daily_pm2p5 = daily_mean.pm2p5.max(dim="date")

        # Identificar a data correspondente ao valor máximo diário
        max_dates = daily_mean.pm2p5.idxmax(dim="date")
        flattened_dates = np.array(max_dates.values).ravel()
        # Remove NaTs ou valores inválidos, se existirem
        valid_dates = flattened_dates[~pd.isnull(flattened_dates)]
        # Converter os valores para datetime64 para garantir compatibilidade
        dates_as_datetime = pd.to_datetime(valid_dates)
        # Obter os meses correspondentes como inteiros
        months_flattened = np.array(
            [date.month for date in dates_as_datetime]
        )  # months_flattened = np.array([int(date.strftime("%Y%m%d%H%M%S")) for date in dates_as_datetime])
        # Criar um array preenchido com NaNs e depois inserir os valores válidos
        months_full = np.full(flattened_dates.shape, np.nan)
        months_full[~pd.isnull(flattened_dates)] = months_flattened
        # Reformar os meses para o formato original de max_dates
        months = xr.DataArray(
            months_full.reshape(
                max_dates.values.shape
            ),  # Reformar para o formato original
            coords=max_dates.coords,  # Mesmas coordenadas que max_dates
            dims=max_dates.dims,  # Mesmas dimensões que max_dates
        )
        # Adicionar os meses ao Dataset original
        max_values = xr.Dataset(
            {"max_value": max_daily_pm2p5, "max_month": months}
        ).transpose("latitude", "longitude")
        max_values.to_netcdf("./Data/Processed/max_values_pm2p5.nc")
        logging.warning("Exporting max pm2p5 to tif.")
        max_daily_pm2p5 = max_daily_pm2p5.transpose("latitude", "longitude")
        max_daily_pm2p5.rio.to_raster("./Data/Processed/max_pm2p5.tif")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    combine_datasets()
