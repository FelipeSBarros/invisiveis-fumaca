# Importação das bibliotecas necessárias
import glob  # Para localizar arquivos com padrões específicos de nome
import os  # Para manipulação de arquivos e diretórios
import zipfile  # Para descompactar arquivos zip
from datetime import datetime  # Para trabalhar com datas
from pathlib import Path  # Para manipulação de caminhos de arquivos

# Para manipulação de datas de forma avançada, como adicionar meses
from dateutil.relativedelta import relativedelta

# Definição das datas de início e fim para o processamento
start_date = datetime(2024, 7, 1).date()  # Data inicial
end_date = datetime(2024, 12, 31).date()  # Data final

# Inicialização da variável para iteração sobre as datas
dt = start_date

# Caminho para onde os arquivos descompactados serão armazenados
dest_path = Path("./Data/Raw/CAMS_AMZ/unzipped")

# Verificação se o diretório de destino existe; se não, cria-o
if not dest_path.exists():
    dest_path.mkdir(parents=True)

# Loop principal para iterar sobre as datas dentro do intervalo
while dt < end_date:
    # Utiliza o glob para encontrar arquivos com o nome que começa com 'cams_' e a data do mês atual
    files = glob.glob(f"./Data/Raw/CAMS_AMZ/cams_{dt}*")

    # Cria um diretório específico para o mês atual dentro do diretório de destino
    intermediate_path = Path.joinpath(dest_path, str(dt))

    # Para cada arquivo encontrado para o mês atual, realiza a extração
    for file in files:
        # Converte o caminho do arquivo para um objeto Path
        file = Path(file)

        # Extrai informações sobre o horário do modelo e o passo de previsão a partir do nome do arquivo
        model_time = file.name.split("_")[2]  # Exemplo: 00:00, 12:00
        step = file.name.split("_")[3].split(".")[0]  # Exemplo: 6, 12

        # Abre o arquivo zip para descompactação
        with zipfile.ZipFile(file, "r") as zip_ref:
            # Extrai todos os arquivos do zip para o diretório do mês correspondente
            zip_ref.extractall(intermediate_path)

        # Renomeia o arquivo extraído para um formato mais organizado
        # Localiza o arquivo .nc extraído (geralmente é o primeiro arquivo que começa com 'data')
        os.rename(
            glob.glob(f"{intermediate_path}/data*.nc")[0],
            # Renomeia o arquivo extraído com base na data, passo e horário do modelo
            f"{intermediate_path}/{dt}_{step}_{model_time}.nc",
        )

    # Avança para o próximo mês
    dt += relativedelta(months=1)