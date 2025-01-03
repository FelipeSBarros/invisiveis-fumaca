import xvec
import geopandas as gpd
import xarray as xr

#laoding xarray dataset
ds = xr.load_dataset("./Data/Processed/CAMS_AMZ_combined.nc")
# Calculating yearly mean of pm2p5
yearly_mean = ds.groupby("Brasilia_reference_time.year").mean()
# yearly_mean = yearly_mean.rio.write_crs("EPSG:4326")
# Loading cities limit Amazonia legal
municipios = gpd.read_file("./Data/Raw/IBGE/Mun_Amazonia_Legal_2022.shp")

estats_mensual = yearly_mean.pm2p5.xvec.zonal_stats(
    municipios.geometry,
    x_coords="longitude",
    y_coords="latitude",
    nodata=-9999
)

# municipios["geometry"] = municipios.geometry.simplify(tolerance=0.0001)  # Ajuste a tolerância conforme necessário.
# municipios = municipios.buffer(1e-7)


print(yearly_mean.isnull().any())
print(municipios.geometry.isna().any())

import rasterio.features

# Rasterize as geometrias
transform = yearly_mean.rio.transform()  # Obtenha a transformação
out_shape = yearly_mean.rio.shape  # Forma do raster

rasterized = rasterio.features.rasterize(
    [(geom, 1) for geom in municipios.geometry.values],
    out_shape=out_shape,
    transform=transform,
    fill=0,
    dtype="int32"  # Certifique-se de especificar o tipo de dado correto
)