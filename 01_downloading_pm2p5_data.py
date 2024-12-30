# Importação das bibliotecas necessárias
import cdsapi  # Cliente para acessar os dados do Copernicus
from datetime import date  # Para manipulação de datas
import time as t  # Para controlar os intervalos de tempo entre as requisições
import calendar  # Para obter o último dia de cada mês
from dateutil.relativedelta import relativedelta  # Para manipulação de datas (como avançar meses)
from pathlib import Path  # Para trabalhar com caminhos de arquivos
import logging  # Para registrar logs de execução

# Inicialização do cliente do Copernicus
# importante, ver README para saber mais sobre credenciais de acesso
server = cdsapi.Client()

# Definição do caminho onde os dados serão armazenados
PATH = Path("./Data/Raw/CAMS_AMZ/")

# Parâmetros padrão para a requisição dos dados
PARAMS = {
    "type": "forecast",  # Tipo de dado que estamos buscando
    "format": "netcdf_zip",  # Formato de saída dos dados
    "variable": "particulate_matter_2.5um",  # Variável de interesse: material particulado de 2.5 micrômetros
    "date": f"2024-07-01/2024-11-30",  # Intervalo de datas (inicialmente setado como o intervalo completo)
    "time": [
        "00:00",  # Horários para os quais os dados serão requisitados
        "12:00",
    ],
    "area": [  # Região geográfica de interesse (coordenadas geográficas da Amazônia)
        5.3103480484992946, -74.0264933540878332, -18.0761089985748562, -43.9634603545391229
    ],
    "leadtime_hour": [  # Intervalos de previsão (em horas UTC)
        "0",  # No início da previsão
        "12",  # Meio-dia
        "6",  # Previsão intermediária
    ],
}

# Definição das datas de início e fim para o download dos dados
START_DATE = date(2024, 7, 1)  # Data inicial
END_DATE = date(2024, 12, 31)  # Data final

# Definição dos horários para as requisições
times = ["00:00", "12:00"]

# Inicialização da variável para iteração sobre os meses
dt = START_DATE
dt_end = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])  # Último dia do mês

# Verificação se o diretório de destino já existe; se não, cria-o
if not PATH.exists():
    PATH.mkdir(parents=True)

# Loop principal para iterar sobre os meses do período definido
while dt < END_DATE:
    params = PARAMS.copy()  # Copia os parâmetros iniciais para cada iteração
    dt_end = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])  # Último dia do mês atual
    params[
        "date"] = f'{dt.strftime("%Y-%m-%d")}/{dt_end.strftime("%Y-%m-%d")}'  # Define o intervalo de datas para o mês

    # Loop sobre os horários definidos para cada dia
    for time in times:
        # Atualiza o parâmetro "time" com o valor atual do loop
        params["time"] = time

        # Definir o intervalo de previsão de acordo com o horário
        if time == "00:00":  # Para a hora "00:00", solicita previsões para os passos 6 e 9 horas
            params["leadtime_hour"] = [6, 9]
        else:  # Para a hora "12:00", solicita previsões para os passos "0/3/6/9/12/15"
            params["leadtime_hour"] = [0, 3, 6, 9, 12, 15]

        # Monta o nome do arquivo baseado nos parâmetros da requisição
        file_name = Path(
            f"{PATH}/cams_{params['date'].replace('/', '-')}_{params['time']}_{'-'.join(list(map(str, params['leadtime_hour'])))}.netcdf_zip"
        )

        # Verifica se o arquivo já existe. Se existir, pula a requisição para evitar duplicação
        if file_name.exists():
            logging.warning(f"File {file_name} already exists. Skipping it.")
        else:
            logging.warning(f'Retriving {time} for {params["date"]}')

            # Realiza a requisição de dados ao servidor do Copernicus
            server.retrieve(
                "cams-global-atmospheric-composition-forecasts",  # Nome do produto no Copernicus
                params,  # Parâmetros para a requisição
                file_name,  # Caminho para salvar o arquivo
            )

            # Pausa por 10 segundos para evitar sobrecarga do servidor
            t.sleep(10)

            # Log de confirmação após a requisição
            logging.warning(f'Done {time} for {params["date"]}')

    # Log de confirmação ao final de cada mês
    logging.warning(f"Done {dt}")

    # Avança para o próximo mês
    dt += relativedelta(months=1)
