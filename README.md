# Invisíveis da Fumaça

Repositório criado para gestionar os scripts usados no projeto "Invisíveis da Fumaça" do [InfoAmazonia](https://infoamazonia.org/).

# Aquisição dos dados

## Particulado fino (PM2.5 ou pm2p5)

Os dados foram obtidos do Copernicus Atmosphere Monitoring Service (CAMS).
Do conjunto de dados [_global atmospheric composition forecasts_](https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts) (veja mais informações na [documentação](https://confluence.ecmwf.int/display/CKB/CAMS%3A+Global+atmospheric+composition+forecast+data+documentation) ), foi baixada a variável _Particulate matter d < 2.5 µm (PM2.5)_ (`"cams-global-atmospheric-composition-forecasts"`), usando o script [`01_downloading_pm2p5_data.py`](01_downloading_pm2p5_data.py).
Para poder usar a [API](https://ads.atmosphere.copernicus.eu/how-to-api), é necessário cadastrar-se e, estando logado, acessar a credencial de acesso pessoal, conforme indicado na documentação da API. 

> ATENÇÃO: Para poder executar o script, é necessário ter a crdencial de acesso já configurada e a biblioteca Python `cdsapi` (>=0.7.2) instalada.

* Caso esteja interessado em aprender a manipular tais dados, veja a lista de [tutoriais](https://ecmwf-projects.github.io/copernicus-training-cams/intro.html) deles.

## Focos de calor

Os dados de focos de calor foram baixados do [INPE](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas), dos satélites NPP-375 para a Amazônia Legal, considerando a janela temporal do projeto (01/07/2024 a 31/12/2024).

## Municípios e  setores censitários 2022

Os dados de [municípios](https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/15819-amazonia-legal.html) e [setores censitários](https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html) foram adquiridos do IBGE. Em abmso os casos, considerou-se apenas aqueles que fazem parte da Amazônia Legal.

## Terras Indigenas

Os dados das Terras Indígenas foram baixados do [INCRA](https://www.gov.br/funai/pt-br/atuacao/terras-indigenas/geoprocessamento-e-mapas).

## Localidades indígenas

[Localidades indigenas](https://www.ibge.gov.br/geociencias/downloads-geociencias.html?caminho=organizacao_do_territorio/estrutura_territorial/localidades/localidades_indigenas_2022/Arquivos_vetoriais/LI/shp/UF)

Foram usados os dados espaciais de localização das localidades indígenas. Os demais dados apresentados pelo IBGE (_Tabelas de Resultados
_)são agregados por UF e Município, escalas que não são de interesse para o projeto.

## Localidades Quilombolas

[Localidades Quilombolas](https://www.ibge.gov.br/estatisticas/sociais/trabalho/22827-censo-demografico-2022.html?edicao=40667&t=acesso-ao-produto)

Foram usados os dados espaciais de localização das localidades quilombolas. Os demais dados apresentados pelo IBGE (_Tabelas de Resultados
_) são agregados por UF e Município, escalas que não são de interesse para o projeto.

## Favelas e Comunidades Urbanas

[Favelas e Comunidades Urbanas ](https://www.ibge.gov.br/estatisticas/sociais/trabalho/22827-censo-demografico-2022.html?edicao=41773)

# Acesso aos dados
> Ambos dados estão disponíveis no `geopackage` Limites_Territoriais_AmazoniaLegal.

# Processamento dos dados

Para cada fase de processamento dos dados, foi criado um script Python. A seguir, a descrição de cada um deles:

1. [`01_downloading_pm2p5_data.py`](01_downloading_pm2p5_data.py), baixamos os dados de PM2.5 do CAMS.
2. [`02_unzip_pm2p5_data.py`](02_unzip_pm2p5_data.py) descompacta os arquivos baixados.
3. [`03_combine_pm2p5_data.py`](03_combine_pm2p5_data.py) combina, organiza e padroniza os dados de pm2p5 descompactados em um único arquivo `NetCDF`.
4. [`04_extract_pm2p5_data.py`](04_extract_pm2p5_data.py) extrai os dados de PM2.5 mensais e de toda a temporada para cada teritório a ser considerado: município, setor censitário e terras indígenas da Amazônia Legal.
