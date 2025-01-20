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

## Municípios e setores censitários 2022

Os dados de [municípios](https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/15819-amazonia-legal.html) e [setores censitários](https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html) foram adquiridos do IBGE. Em abmso os casos, considerou-se apenas aqueles que fazem parte da Amazônia Legal.

### Dicionário da tabela de atributos dos setores censitários

| VARIÁVEL 	| CATEGORIAS 	| DESCRIÇÃO 	|
|---	|---	|---	|
| CD_SETOR 	|  	| Geocódigo de Setor Censitário 	|
| SITUACAO 	|  	| Situação do Setor Censitário 	|
|  	| Urbana 	| Urbana 	|
|  	| Rural 	| Rural 	|
| CD_SITUACAO 	|  	| Situação detalhada do Setor Censitário 	|
|  	| 1 	| Área urbana de alta densidade de edificações de cidade ou vila 	|
|  	| 2 	| Área urbana de baixa densidade de edificações de cidade ou vila 	|
|  	| 3 	| Núcleo urbano 	|
|  	| 5 	| Aglomerado rural - Povoado 	|
|  	| 6 	| Aglomerado rural - Núcleo rural 	|
|  	| 7 	| Aglomerado rural - Lugarejo 	|
|  	| 8 	| Área rural (exclusive aglomerados) 	|
|  	| 9 	| Massas de água 	|
| CD_TIPO 	|  	| Tipo do Setor Censitário 	|
|  	| 0 	| Não especial 	|
|  	| 1 	| Favela e Comunidade Urbana 	|
|  	| 2 	| Quartel e base militar 	|
|  	| 3 	| Alojamento / acampamento 	|
|  	| 4 	| Setor com baixo patamar domiciliar 	|
|  	| 5 	| Agrupamento indígena 	|
|  	| 6 	| Unidade prisional 	|
|  	| 7 	| Convento / hospital / ILPI / IACA 	|
|  	| 8 	| Agrovila do PA 	|
|  	| 9 	| Agrupamento quilombola 	|
| AREA_KM2 	|  	| Área do Setor Censitário em quilômetros quadrados 	|
| CD_REGIAO 	|  	| Código das Grandes Regiões (Regiões Geográficas) 	|
| NM_REGIAO 	|  	| Nome das Grandes Regiões (Regiões Geográficas) 	|
| CD_UF 	|  	| Código da Unidade da Federação 	|
| NM_UF 	|  	| Nome da Unidade da Federação 	|
| CD_MUN 	|  	| Código do Município 	|
| NM_MUN 	|  	| Nome do Município 	|
| CD_DIST 	|  	| Código do Distrito 	|
| NM_DIST 	|  	| Nome do Distrito 	|
| CD_SUBDIS 	|  	| Código do Subdistrito 	|
| NM_SUBDIST 	|  	| Nome do Subdistrito 	|
| CD_BAIRRO 	|  	| Código do Bairro 	|
| NM_BAIRRO 	|  	| Nome do Bairro 	|
| CD_NU 	|  	| Código do Núcleo Urbano 	|
| NM_NU 	|  	| Nome do Núcleo Urbano 	|
| CD_FCU 	|  	| Código da Favela ou Comunidade Urbana 	|
| NM_FCU 	|  	| Nome da Favela ou Comunidade Urbana 	|
| CD_AGLOM 	|  	| Código do Aglomerado 	|
| NM_AGLOM 	|  	| Nome do Aglomerado 	|
| CD_RGINT 	|  	| Código da Região Geográfica Intermediária 	|
| NM_RGINT 	|  	| Nome da Região Geográfica Intermediária 	|
| CD_RGI 	|  	| Código da Região Geográfica Imediata 	|
| NM_RGI 	|  	| Nome da Região Geográfica Imediata 	|
| CD_CONCURB 	|  	| Código da Concentração Urbana 	|
| NM_CONCURB 	|  	| Nome da Concentração Urbana 	|
| V0001 	|  	| Total de pessoas 	|
| V0002 	|  	| Total de Domicílios (DPPO + DPPV + DPPUO + DPIO + DCCM + DCSM) 	|
| V0003 	|  	| Total de Domicílios Particulares (DPPO + DPPV + DPPUO + DPIO) 	|
| V0004 	|  	| Total de Domicílios Coletivos (DCCM + DCSM) 	|
| V0005 	|  	| Média de moradores em Domicílios Particulares Ocupados (Total pessoas em Domicílios Particulares Ocupados / DPPO + DPIO) 	|
| V0006 	|  	| Percentual de Domicílios Particulares Ocupados Imputados (Total DPO imputados / Total DPO) 	|
| V0007 	|  	| Total de Domicílios Particulares Ocupados (DPPO + DPIO) 	|

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

### Dicionário de atributos das localidades quilombolas

| VARIÁVEL 	| TIPO 	| TAMANHO 	| DESCRIÇÃO 	|
|---	|---	|---	|---	|
| CD_UF 	| numérico 	| 2 	| Geocódigo da Unidade da Federação 	|
| NM_UF 	| texto 	| 20 	| Nome da Unidade da Federação 	|
| SG_UF 	| texto 	| 2 	| Sigla da Unidade da Federação 	|
| CD_MUNIC 	| numérico 	| 7 	| Geocódigo do município 	|
| NM_MUNIC 	| texto 	| 50 	| Nome do município 	|
| IDCQ0001 	| texto 	| 5 	| Código único nacional da Comunidade Quilombola declarada com localidade associada 	|
| OCORRENCIA 	| numérico 	| 1 	| Ordem de ocorrência da Localidade Quilombola no Município 	|
| CD_LQ 	| texto 	| 12 	| Código municipal da Localidade Quilombola associada à Comunidade Quilombola declarada 	|
| PREFIXO 	| texto 	| 21 	| Prefixo geral das Comunidades Quilombolas com localidade associada 	|
| NM_LQ 	| texto 	| 100 	| Nome da Comunidade Quilombola declarada com localidade associada 	|
| CD_AGLOM 	| texto 	| 5 	| Código do agrupamento quilombola 	|
| NM_AGLOM 	| texto 	| 100 	| Nome do agrupamento quilombola 	|
| CD_TQ 	| numérico 	| 3 	| Código do Território Quilombola oficialmente delimitado 	|
| NM_TQ 	| texto 	| 60 	| Nome do Território Quilombola oficialmente delimitado 	|
| P_FCP 	| texto 	| 70 	| Número do processo de identificação e reconhecimento na Fundação Cultural Palmares 	|
| Lat_d 	| numérico 	| 20 	| Latitude em graus decimais 	|
| Long_d 	| numérico 	| 20 	| Longitude em graus decimais 	|
| Nota: O CD_LQ é resultante da união entre CD_MUNIC, IDLQ0001 e OCORRENCIA. 	|  	|  	|  	|

## Favelas e Comunidades Urbanas

[Favelas e Comunidades Urbanas ](https://www.ibge.gov.br/estatisticas/sociais/trabalho/22827-censo-demografico-2022.html?edicao=41773)

# Acesso aos dados
> Ambos dados estão disponíveis no `geopackage` Limites_Territoriais_AmazoniaLegal.

# Processamento dos dados

Para cada fase de processamento dos dados, foi criado um script Python. A seguir, a descrição de cada um deles:

1. [`01_downloading_pm2p5_data.py`](01_downloading_pm2p5_data.py), baixamos os dados de PM2.5 do CAMS.
2. [`02_unzip_pm2p5_data.py`](02_unzip_pm2p5_data.py) descompacta os arquivos baixados.
3. [`03_combine_pm2p5_data.py`](03_combine_pm2p5_data.py) combina, organiza e padroniza os dados de pm2p5 descompactados em um único arquivo `NetCDF`.
4. [`04_extract_pm2p5_data.py`](04_extract_pm2p5_data.py) extrai os dados de PM2.5 mensais e de toda a temporada para cada teritório a ser considerado: município, setor censitário e terras indígenas, localidades indígenas, localidades quilombolas e favelas e comunidades urbanas, da Amazônia Legal.
5. [`05_finding_communities`](05_finding_communities.py) Identifica, dos territórios analizados, aqueles 10% mais afetados.
