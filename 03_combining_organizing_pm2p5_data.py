import xarray as xr  # Importa o xarray para trabalhar com datasets multidimensionais
from glob import glob  # Importa glob para buscar arquivos no sistema
import pandas as pd  # Importa pandas para manipulação de datas e tempos
import numpy as np  # Importa numpy para operações numéricas

# 1. Obtenha a lista de arquivos NetCDF presentes em um diretório e subdiretórios.
datasets = glob("./Data/Raw/CAMS_AMZ/unzipped/*/*.nc")

# 2. Crie uma lista para armazenar os datasets processados
processed_datasets = []

# 3. Itere sobre cada arquivo NetCDF para carregar e processar os dados
for file in datasets:
    ds = xr.open_dataset(file)  # Carrega o dataset do arquivo NetCDF

    # 4. Converter a variável 'forecast_reference_time' para pandas datetime
    # A 'forecast_reference_time' indica o momento de referência da previsão.
    forecast_reference_time_pandas = pd.to_datetime(
        ds["forecast_reference_time"].values
    )

    # 5. Converter a variável 'forecast_period' para timedelta
    # 'forecast_period' é o tempo relativo da previsão, que é em horas. Vamos convertê-lo para o formato timedelta.
    forecast_period_timedelta = pd.to_timedelta(ds["forecast_period"].values, unit="h")

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
    # Primeiramente, convertemos para o fuso horário UTC, depois para o horário de Brasília e removemos a informação de fuso horário.
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

    # 11. Calcular o número total de elementos do conjunto de dados (não usado diretamente aqui, mas calculado para fins de verificação)
    num_elements = (
        combined_times.shape[0] * combined_times.shape[1]
    )  # Número total de combinações

    # 12. Colapsar as dimensões 'forecast_reference_time' e 'forecast_period' em uma nova dimensão 'flat_time'
    # Isso cria uma única dimensão combinando as duas dimensões anteriores, simplificando o acesso aos dados
    ds = ds.stack({"flat_time": ("forecast_reference_time", "forecast_period")})

    # 13. Adicionar a nova coordenada 'Brasilia_reference_time' associada à nova dimensão 'flat_time'
    ds = ds.assign_coords({"Brasilia_reference_time": ("flat_time", combined_times_1d)})

    # 14. Substituir a dimensão antiga 'flat_time' pela nova dimensão 'Brasilia_reference_time'
    ds = ds.swap_dims({"flat_time": "Brasilia_reference_time"})

    # 15. Remover as dimensões e variáveis antigas que não são mais necessárias
    # A remoção inclui as variáveis 'forecast_reference_time', 'forecast_period', 'valid_time', e 'flat_time'
    ds = ds.drop_vars(
        ["forecast_reference_time", "forecast_period", "valid_time", "flat_time"]
    )

    # 16. Adicionar o dataset processado à lista de datasets
    processed_datasets.append(ds)

# 17. Concatenar todos os datasets processados ao longo da nova dimensão 'Brasilia_reference_time'
ds = xr.concat(processed_datasets, dim="Brasilia_reference_time")

# 18. Converter os valores de 'pm2p5' de unidades de 'mol/m³' para 'ug/m³'
ds["pm2p5"] = (
    ds["pm2p5"] * 1e9
)  # Multiplica por 1 bilhão (10^9) para converter de mol para microgramas

# 19. Atualizar os atributos do dataset para refletir as novas unidades
ds.attrs["units"] = "ug/m3"

# 20. Salvar o dataset final em um novo arquivo NetCDF
ds.to_netcdf("./Data/Processed/CAMS_AMZ_combined.nc")
