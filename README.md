# Invisíveis da Fumaça

Repositório criado para gestionar os scripts usados no projeto "Invisíveis da Fumaça" do [InfoAmazonia](https://infoamazonia.org/).

# Aquisição dos dados

## Focos de calor

Os dados de focos de calor foram baixados do [INPE](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas), dos satélites NPP-375 para a Amazônia Legal, considerando a janela temporal do projeto (01/07/2024 a 31/12/2024).

O arquivo baixado foi o [`focos_qmd_inpe_2024-07-01_2024-12-31_01.405022.geojson`](Data/Raw/NPP-375/focos_qmd_inpe_2024-07-01_2024-12-31_10.005470.geojson).

## Particulado fino

Os dados foram obtidos do Copernicus Atmosphere Monitoring Service (CAMS).
Do conjunto de dados [_global atmospheric composition forecasts_](https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts) (veja mais informações na [documentação](https://confluence.ecmwf.int/display/CKB/CAMS%3A+Global+atmospheric+composition+forecast+data+documentation) ), foi baixada a variável _Particulate matter d < 2.5 µm (PM2.5)_ (`"cams-global-atmospheric-composition-forecasts"`), usando o script [`01_downloading_pm2p5_data.py`](01_downloading_pm2p5_data.py).
Para poder usar a [API](https://ads.atmosphere.copernicus.eu/how-to-api), é necessário cadastrar-se e, estando logado, acessar a credencial de acesso pessoal, conforme indicado na documentação da API. 

> ATENÇÃO: Para poder executar o script, é necessário ter a crdencial de acesso já configurada e a biblioteca Python `cdsapi` (>=0.7.2) instalada.

* Caso esteja interessado em aprender a manipular tais dados, veja a lista de [tutoriais](https://ecmwf-projects.github.io/copernicus-training-cams/intro.html) deles.

# Malha de setores censitários 2022
A malha espaciald e setores censitários foram obtidos do site do [IBGE](https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html).
Os dados de municípios foram adquiridos [nesta página do IBGE](https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/15819-amazonia-legal.html)
