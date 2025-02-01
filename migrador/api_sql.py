import brotli
import requests
import datetime
import os
from dotenv import load_dotenv
from base64 import urlsafe_b64encode

load_dotenv()

SQL_API_URL = os.getenv("SQL_API_URL")


def get_query(consortium, queryType, data_inicio, data_fim):
    match queryType:
        case "viagens":
            return f"SELECT SUM(PassageirosDia) AS totalViagens, Data AS data, TipoDia AS tipoDia FROM ind_passageiros_dia WHERE lower(Consorcio) IN ('{consortium}') AND Data BETWEEN epoch_ms({data_inicio}) AND epoch_ms({data_fim}) GROUP BY Data, TipoDia ORDER BY Data"
        case "quilometragem-ida":
            return f"""SELECT Linha AS numeroLinha, SUM(KmProgramadaIda) AS kmProgramadaIda, SUM(KmRealizadaIda) AS kmRealizadaIda, FROM ind_km_realizada WHERE Ano BETWEEN EXTRACT(YEAR FROM epoch_ms({data_inicio})) AND EXTRACT(YEAR FROM epoch_ms({data_fim})) AND Data BETWEEN epoch_ms({data_inicio}) AND epoch_ms({data_fim}) AND lower(Consorcio) IN ('{consortium}') GROUP BY Linha ORDER BY Linha"""
        case "quilometragem-volta":
            return f"""SELECT Linha AS numeroLinha, SUM(KmProgramadaVolta) AS kmProgramadaVolta, SUM(KmRealizadaVolta) AS kmRealizadaVolta, FROM ind_km_realizada WHERE Ano BETWEEN EXTRACT(YEAR FROM epoch_ms({data_inicio})) AND EXTRACT(YEAR FROM epoch_ms({data_fim})) AND Data BETWEEN epoch_ms({data_inicio}) AND epoch_ms({data_fim}) AND lower(Consorcio) IN ('{consortium}') GROUP BY Linha ORDER BY Linha"""
        case "frota":
            return f"""WITH base AS (SELECT Linha,
                               Data,
                               LIST_UNIQUE(FLATTEN(LIST(BlockIds))) AS "frotaProgramada",
                               LIST_UNIQUE(FLATTEN(LIST(Veiculos))) AS "frotaDisponivel",
                        FROM ind_idf
                        WHERE Ano BETWEEN EXTRACT(YEAR FROM epoch_ms({data_inicio})) AND EXTRACT(YEAR FROM epoch_ms({data_fim})) -- necessário para o particionamento
                          AND Data BETWEEN epoch_ms({data_inicio}) AND epoch_ms({data_fim})
                          AND lower(Consorcio) IN ('{consortium}')
                        GROUP BY Linha,
                                 Data)
                        SELECT Linha                                              AS "linha",
                                ROUND(SUM(frotaProgramada) / COUNT(DISTINCT data)) AS "frotaProgramada",
                                ROUND(SUM(frotaDisponivel) / COUNT(DISTINCT data)) AS "frotaDisponivel"
                        FROM base
                        GROUP BY Linha
                        ORDER BY Linha"""


def get_first_and_last_day_previous_month(month=None, year=None):
    now = datetime.datetime.now()
    now = now.replace(
        day=1, month=month if month else now.month, year=year if year else now.year
    )  # forçando a ser dia 1 do mês que a automação rodar
    data_fim = now - datetime.timedelta(days=1)
    data_inicio = data_fim.replace(day=1) - datetime.timedelta(days=1)
    return int(data_inicio.timestamp() * 1000), int(data_fim.timestamp() * 1000)


def get_from_api(consortium, queryType):
    data_inicio, data_fim = get_first_and_last_day_previous_month(month=12, year=2024)
    query = get_query(consortium, queryType, data_inicio, data_fim)
    query_brotli = brotli.compress(query.encode("utf-8"))
    query_safe = urlsafe_b64encode(query_brotli).decode()
    url_query = SQL_API_URL + query_safe
    result = requests.get(url_query)
    return result.json()


if __name__ == "__main__":
    result = get_from_api("transoceânico", "frota")
    print(result)
