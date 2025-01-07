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


# Item 2- Quilometragem programada x realizada

# Ida
url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/dados-operacionais/quilometragem/programada-ida?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

response_ida = requests.get(url).json()
df_ida = pd.DataFrame.from_dict(response_ida["dados"])

# Volta
url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/dados-operacionais/quilometragem/programada-volta?Linhas={linhas}&Threshold={treshold}&from={inicio}&to={fim}"

response_volta = requests.get(url).json()
df_volta = pd.DataFrame.from_dict(response_volta["dados"])

# Merge Ida and Volta on 'numeroLinha'
df_totais = pd.merge(df_ida, df_volta, on='numeroLinha', suffixes=('_ida', '_volta'))

# Calculate total_programada and total_realizada
df_totais['total_programada'] = round(df_totais['kmProgramadaIda'] + df_totais['kmProgramadaVolta'], 2)
df_totais['total_realizada'] = round(df_totais['kmRealizadaIda'] + df_totais['kmRealizadaVolta'], 2)

# Select relevant columns
df_totais = df_totais[['numeroLinha', 'total_programada', 'total_realizada']]
df_totais.rename(columns={'numeroLinha': 'linha'}, inplace=True)

# Calcula a porcentagem da Escala de Cumprimento
compliance_km = df_totais['total_realizada'].sum() / df_totais['total_programada'].sum()
print(compliance_km)
porcentagem_conclusao = round((compliance_km * 100), 2)
print(porcentagem_conclusao)
subsidio_concedido = calcular_subsidio(compliance_km * 100)
print(subsidio_concedido)

json_totais = df_totais.to_json(orient='records')

payload = {
    "dados": json_totais,
    "tipoInput": "compliance/quilometragem_percorrida"
}
# print(payload)
response_binario = json.dumps(payload, indent=2).encode('utf-8')
print(response_binario)