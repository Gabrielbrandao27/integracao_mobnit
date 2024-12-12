import requests


MOBNIT_API_URL = "https://mobnit.niteroi.rj.gov.br/api/website/v1"
MANAGER_TOKEN = "qkiybj2rx8rwnn6cnhyweiwx6bt1kq5e"
linhas = f"%2735%27%2C%2734A%27"
treshold = f"%270%27"
inicio = "1727740800000"
fim = "1730419199999"


def km_programada(linhas, treshold, inicio, fim):
    # Item 2- Quilometragem programada

    # ida
    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/auditoria/quilometragem/programada-ida?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

    response = requests.get(url).json()

    struct_km = {
        "ida": [],
        "volta": [],
        "totais": []
    }

    for item in response["dados"]:
        struct_km["ida"].append(item)

    # volta
    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/auditoria/quilometragem/programada-volta?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

    response = requests.get(url).json()
    
    for item in response["dados"]:
        struct_km["volta"].append(item)

    for ida in struct_km["ida"]:
        for volta in struct_km["volta"]:
            if ida["numeroLinha"] == volta["numeroLinha"]:
                struct_km["totais"].append(
                    {
                        "linha": ida["numeroLinha"],
                        "total_programada": ida["kmProgramadaIda"] + volta["kmProgramadaVolta"],
                        "total_realizada": ida["kmRealizadaIda"] + volta["kmRealizadaVolta"]
                    }
                )

    return struct_km


def quantiade_onibus(treshold, inicio, fim):
    # Item 4- Quantidade de ônibus programada
    treshold = f"%270%27"
    inicio = f"1727740800000"
    fim = "1730419199999"
    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/indicadores/frota/disponivel-programada?Threshold={treshold}&from={inicio}&to={fim}"

    response = requests.get(url).json()

    print(response)


print(km_programada(linhas, treshold, inicio, fim))