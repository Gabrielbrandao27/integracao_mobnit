import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

MOBNIT_API_URL = os.getenv('MOBNIT_API_URL')
MANAGER_TOKEN = os.getenv('MANAGER_TOKEN')

# Parâmetros para as requisições
linhas = f"%2735%27%2C%2734A%27"
treshold = f"%270%27"
inicio = f"1727740800000"
fim = "1730419199999"
empresas = 'Transportes Peixoto Ltda'

def calcular_subsidio(compliance):

    if 100 <= compliance and compliance >= 95:
        return 100
    if 94 <= compliance and compliance >= 90:
        return 95
    if 89 <= compliance and compliance >= 85:
        return 85
    if 84 <= compliance and compliance >= 80:
        return 70
    return 0


# Item 4- Quantidade de ônibus programada x realizada

url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/indicadores/frota/disponivel-programada?Threshold={treshold}&from={inicio}&to={fim}&Empresas={empresas}"

response = requests.get(url).json()

dados_onibus_df = pd.DataFrame.from_dict(response['dados'])

# Calcula total de frotas programadas e disponíveis
frota_programada = dados_onibus_df['frotaProgramada'].sum()
frota_disponivel = dados_onibus_df['frotaDisponivel'].sum()

# Cria novo DataFrame com os totais por Consórcio
dados_onibus_df = pd.DataFrame({'total_frotas_programadas': [frota_programada], 'total_frotas_disponiveis': [frota_disponivel]})
print(dados_onibus_df)

# Calcula a porcentagem da Escala de Cumprimento
compliance_frota = round((frota_disponivel / frota_programada), 2)
print(compliance_frota)

json_totais = dados_onibus_df.to_json(orient='records')

# Calcula a porcentagem do Subsídio
subsidio_concedido = calcular_subsidio(compliance_frota * 100)

# subsidios_totais(subsidio_struct['dados'], 'bus_amount', valor_compliance, subsidio_concedido)

payload = {
    "tipoInput": "compliance/frota_disponivel",
    "dados": {
        "consorcio": "TransNit",
        "compliance": json_totais,
        "porcentagem_conclusao": compliance_frota,
        "subsidio_concedido": subsidio_concedido,
    }
}

# Transforma response em Binário para enviar ao dApp
# response_binario = json.dumps(response, indent=2).encode('utf-8')

print(payload)


# Item 2- Quilometragem programada x realizada

# Ida
url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/dados-operacionais/quilometragem/programada-ida?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

response_ida = requests.get(url).json()
df_ida = pd.DataFrame.from_dict(response_ida["dados"])

# Volta
url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/dados-operacionais/quilometragem/programada-volta?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

response_volta = requests.get(url).json()
df_volta = pd.DataFrame.from_dict(response_volta["dados"])

# Merge Ida e Volta em 'numeroLinha'
df_totais = pd.merge(df_ida, df_volta, on='numeroLinha', suffixes=('_ida', '_volta'))

# Calcula total_programada e total_realizada
total_programada = round(df_totais['kmProgramadaIda'] + df_totais['kmProgramadaVolta'], 2).sum()
total_realizada = round(df_totais['kmRealizadaIda'] + df_totais['kmRealizadaVolta'], 2).sum()

# Cria novo DataFrame com os totais por Consórcio
df_totais = pd.DataFrame({'total_programada': [total_programada], 'total_realizada': [total_realizada]})

# Calcula a porcentagem da Escala de Cumprimento
compliance_km = round((total_realizada / total_programada), 2)
print(compliance_km)
subsidio_concedido = calcular_subsidio(compliance_km * 100)
print(subsidio_concedido)

json_totais = df_totais.to_json(orient='records')

payload = {
    "tipoInput": "compliance/quilometragem_percorrida",
    
    "dados": {
        "consorcio": "TransNit",
        "compliance": json_totais,
        "porcentagem_conclusao": compliance_km,
        "subsidio_concedido": subsidio_concedido
    }
}

print(payload)