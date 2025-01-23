import matplotlib.pyplot as plt
import geopandas as gpd
import xarray as xr
import logging


def create_figs():
    # Carregando o arquivo de resultados
    logging.warning("Carregando resultados e Datasets.")
    # gpd.list_layers('./Data/Processed/results.gpkg')
    amz_muns = gpd.read_file(
        "./Data/Processed/results.gpkg", layer="Municipios_2022_pm2p5"
    )
    amz_setores = gpd.read_file(
        "./Data/Processed/results.gpkg", layer="Setores_Censitarios_2022_pm2p5"
    )
    amz_tis = gpd.read_file(
        "./Data/Processed/results.gpkg", layer="TerrasIndigenas_2022_pm2p5"
    )
    # gpd.list_layers('./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg')
    amz_uf = gpd.read_file(
        "./Data/Raw/IBGE/Limites_Territoriais_AmazoniaLegal.gpkg", layer="Estados"
    )

    ds = xr.load_dataset("./Data/Processed/CAMS_AMZ_combined.nc")
    daily_mean = ds.groupby("Brasilia_reference_time.date").mean()
    monthly_mean = ds.groupby("Brasilia_reference_time.month").mean()
    monthly_mean = monthly_mean.pm2p5.transpose("month", "latitude", "longitude")
    median = ds.pm2p5.median(dim="Brasilia_reference_time")
    median = median.transpose("latitude", "longitude")
    mean = ds.pm2p5.mean(dim="Brasilia_reference_time")
    mean = mean.transpose("latitude", "longitude")
    days_above_15 = ds.groupby("Brasilia_reference_time.date").mean().pm2p5 > 15
    days_above_15 = days_above_15.sum(dim="date", skipna=True)
    days_above_15 = days_above_15.transpose("latitude", "longitude")
    days_above_15 = days_above_15.rio.write_crs("EPSG:4326")
    days_above_15 = days_above_15.astype("int32")
    max_pm2p5 = daily_mean.pm2p5.max(dim="date")
    max_pm2p5 = max_pm2p5.transpose("latitude", "longitude")

    logging.warning("Criando imagem de de média mensal")
    # plot monthly mean:
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
    axes = axes.flatten()
    months = ["Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    for i, month in enumerate(monthly_mean.month):
        monthly_mean.sel(month=month).plot(ax=axes[i], cmap="viridis")
        axes[i].set_title(f"{months[i]}")
        amz_uf.plot(ax=axes[i], facecolor="none", edgecolor="black")
    # plt.tight_layout()
    plt.savefig("./figs/monthly_mean_pm2p5.png")

    logging.warning("Criando imagem de mediana")
    level = [0, 10, 15, 25, 50, 75, 180]
    f, ax = plt.subplots(1, 2, figsize=(20, 10))
    median.plot(ax=ax[0])
    amz_uf.plot(ax=ax[0], facecolor="none", edgecolor="black")
    ax[0].title.set_text("Valor mediano de PM2.5")
    median.plot(levels=level, ax=ax[1])
    amz_uf.plot(ax=ax[1], facecolor="none", edgecolor="black")
    ax[1].title.set_text("Valor mediano de PM2.5")
    # plt.tight_layout()
    plt.savefig("./figs/median_pm2p5.png")

    logging.warning("Criando imagem de maior valor diário")
    f, ax = plt.subplots(1, 2, figsize=(20, 10))
    max_pm2p5.plot(ax=ax[0])
    amz_uf.plot(ax=ax[0], facecolor="none", edgecolor="black")
    ax[0].title.set_text("Maior valor diário de PM2.5")
    days_above_15.plot(ax=ax[1], levels=[0, 30, 60, 90, 120, 150, 180])
    amz_uf.plot(ax=ax[1], facecolor="none", edgecolor="black")
    ax[1].title.set_text("Quantidade de dias com PM2.5 acima de 15")
    plt.savefig("./figs/max_pm2p5.png")

    logging.warning("Criando imagem de média")
    f, ax = plt.subplots(1, 2, figsize=(20, 10))
    mean.plot(ax=ax[0])
    amz_uf.plot(ax=ax[0], facecolor="none", edgecolor="black")
    ax[0].title.set_text("Valor médio de PM2.5")
    mean.plot(levels=level, ax=ax[1])
    amz_uf.plot(ax=ax[1], facecolor="none", edgecolor="black")
    ax[1].title.set_text("Valor médio de PM2.5")
    plt.savefig("./figs/mean_pm2p5.png")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    create_figs()
