# Importando bibliotecas necessárias
import xvec
import geopandas as gpd
import xarray as xr

# Carregando o dataset XArray
# Usei `open_dataset` em vez de `load_dataset`, pois o último carrega tudo na memória.
ds = xr.open_dataset("./Data/Processed/CAMS_AMZ_combined.nc")

# Calculando a média anual do PM2.5
# A função `groupby` organiza os dados por ano e `mean` calcula a média.
yearly_mean = ds.groupby("Brasilia_reference_time.year").mean()

# Calculando a média mensal do PM2.5 e salvando o resultado
monthly_mean = ds.groupby("Brasilia_reference_time.month").mean()
monthly_mean.to_netcdf("./Data/Processed/CAMS_AMZ_monthly_mean.nc")

# Carregando os limites dos municípios da Amazônia Legal
municipios = gpd.read_file("./Data/Raw/IBGE/Mun_Amazonia_Legal_2022.shp")

# Convertendo o sistema de referência para EPSG:4326
municipios.to_crs(epsg=4326, inplace=True)

# Calculando estatísticas zonais para a média mensal
# O método `exactextract` garante precisão ao cruzar o raster com as geometrias.
estats_mensual = monthly_mean.xvec.zonal_stats(
    municipios.geometry,
    x_coords="longitude",
    y_coords="latitude",
    method="exactextract",
)

# Convertendo os resultados das estatísticas zonais para um GeoDataFrame
df_ = estats_mensual.xvec.to_geodataframe(name="pm2p5").reset_index()

# Adicionando um ID único para cada município por mês
df_["id"] = df_.groupby("month").cumcount()

# Removendo a coluna de geometria, já que não será usada na transformação para formato "wide"
df_ = df_.drop(columns=["geometry"])

# Transformando o DataFrame para formato "wide" (colunas por mês)
df_wide = df_.pivot(columns="month", index="id", values="pm2p5")

# Renomeando as colunas para os meses correspondentes
df_wide.columns = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

# Fazendo o join com os limites dos municípios
# A opção `inner` garante que apenas os municípios com dados sejam mantidos.
merged_df = municipios.join(df_wide, how="inner")

# Exibindo o DataFrame final para verificar os resultados
merged_df.to_file("./Data/Processed/results.gpkg", layer='Municipios_PM2.5_Mensal', driver="GPKG")