# Invisíveis da Fumaça

Invisíveis da Fumaça é um projeto especial do [InfoAmazonia](https://infoamazonia.org/). Nele, usamos dados de particulado fino (PM2.5) para analisar a exposição de comunidades vulneráveis da Amazônia Legal à poluição do ar.

Neste repositório, você encontrará os scripts usados para baixar, processar e analisar os dados de PM2.5, bem como os resultados encontrados.

# Tabela de conteúdos

* [Invisíveis da Fumaça](#invisíveis-da-fumaça)
* [Resultados](#resultados)

Caso queira conhecer a metodologia do projeto e, quem sabe, replicá-lo, os seguintes tópicos podem ajudar:

* [Aquisição dos dados](#aquisição-dos-dados)
* [Processamento dos dados](#processamento-dos-dados)

# Resultados

Um mapa web foi criado com os valores de PM2.5 médio para todo o período e a cada mês, com as Localidades Indígenas, Quilombolas e Favelas e comunidades urbanas da Amazônia Legal. 
* [Média temporada](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/media_temporada/#5/-6.494/-57.893)
* [Julho](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Jul/)
* [Agosto](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Ago/)
* [Setembro](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Set/)
* [Outubro](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Out/)
* [Novembro](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Nov/)
* [Dezembro](https://felipesbarros.github.io/invisiveis-fumaca/WebMap/Dez/)

# Aquisição dos dados

Aqui apresentaremos como foram adquiridos e usados os dados do projeto.

> Todos os dados estão disponíveis no `geopackage` Limites_Territoriais_AmazoniaLegal.

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

### Dicionário de atributos das localidades indígenas

| VARIÁVEL 	| CATEGORIAS 	| DESCRIÇÃO 	|
|---	|---	|---	|
| CD_UF 	|  	| Código da Unidade da Federação 	|
| NM_UF 	|  	| Nome da Unidade da Federação 	|
| CD_MUNIC 	|  	| Código do Município 	|
| NM_MUNIC 	|  	| Nome do município 	|
| ID_LI 	|  	| Identificador único por registro de ocorrência de Localidade Indígena ou do Local de Concentração de Pessoas Indígenas 	|
| CD_LI 	|  	| Código único nacional de Localidade Indígena ou do Local de Concentração de Pessoas Indígenas 	|
| OCORRENCIA 	|  	| Ordem de ocorrência da Localidade Indígena ou do Local de Concentração de Pessoas Indígenas no Município 	|
| NM_LI 	|  	| Nome da Localidade Indígena ou do Local de Concentração de Pessoas Indígenas 	|
| CD_SETOR 	|  	| Geocódigo de Setor Censitário 	|
| SITUACAO 	|  	| Situação do Setor Censitário 	|
|  	| Urbana 	| Urbana 	|
|  	| Rural 	| Rural 	|
| CD_SIT 	|  	| Situação detalhada do Setor Censitário 	|
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
| CD_AGLOM 	|  	| Código de Aglomerado associado ao Setor Censitário de Agrupamento Indígena 	|
| NM_AGLOM 	|  	| Nome Aglomerado associado ao Setor Censitário de Agrupamento Indígena 	|
| CD_TI 	|  	| Código da Terra Indígena no IBGE 	|
| TI_FUNAI 	|  	| Código da Terra Indígena nos arquivos vetoriais da Funai 	|
| NM_TI 	|  	| Nome da Terra Indígena 	|
| FASE 	|  	| Situação fundiária da Terra Indígena 	|
| C_CR_FUNAI 	|  	| Código da Coordenação Regional da Funai 	|
| N_CR_FUNAI 	|  	| Nome da Coordenação Regional da Funai 	|
| ALD_FUNAI 	|  	| Código da Aldeia Indígena no arquivos vetoriais da Funai 	|
| VAL_FUNA 	|  	| Tipo de validação da interoperabilidade entre a Localidade Indígena e o respectivo código nos arquivos vetoriais de Aldeias Indígenas mantido pela Funai 	|
|  	| 1 	| Validação espacial e cadastral 	|
|  	| 2 	| Validação cadastral 	|
| ALD_SIASI 	|  	| Código no arquivo vetorial do Sistema de Informações da Atenção à Saúde Indígena (Siasi) 	|
| VAL_SIAS 	|  	| Tipo de validação da interoperabilidade entre a Localidade Indígena e o respectivo código no arquivo vetorial do Siasi 	|
|  	| 1 	| Validação espacial e cadastral 	|
|  	| 2 	| Validação cadastral 	|
| AMZ_LEG 	|  	| Indicador de localização nos limites da Amazônia Legal 	|
|  	| 1 	| Localizada na Amazônia Legal 	|
| LAT 	|  	| Latitude em graus decimais 	|
| LONG 	|  	| Longitude em graus decimais 	|

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

# Processamento dos dados

Para cada fase de processamento dos dados, foi criado um script Python. A seguir, o link e breve a descrição de cada um deles:

1. [`01_downloading_pm2p5_data.py`](01_downloading_pm2p5_data.py): script usado para automatizar a requisição e o download baixamos dos dados de PM2.5 do CAMS.
2. [`02_unzip_pm2p5_data.py`](02_unzip_pm2p5_data.py): script criado para automatizar a organização dos dados de PM2.5 baixados do CAMS. Ele descompacta os arquivos baixados.
3. [`03_combine_pm2p5_data.py`](03_combine_pm2p5_data.py): Script que combina, organiza e padroniza os dados de PM2.5 descompactados. Como resultado teremos um único arquivo `NetCDF` com todos os dados, outros dois netCDFs com a média de PM2.5 para a temporada e a média mensal.
4. [`04_extract_pm2p5_data.py`](04_extract_pm2p5_data.py) extrai os dados de PM2.5 mensais e de toda a temporada para cada teritório a ser considerado: município, setor censitário e terras indígenas, localidades indígenas, localidades quilombolas e favelas e comunidades urbanas, da Amazônia Legal.
5. [`05_finding_communities`](05_finding_communities.py) Identifica, dos territórios analisados, aqueles 10% mais afetados.
