import requests
import pandas as pd
import json
import os
# from eth_abi import encode_abi
from web3 import Web3
from dotenv import load_dotenv
from get_from_excel import get_consortium_compliance

load_dotenv()

MOBNIT_API_URL = os.getenv('MOBNIT_API_URL')
MANAGER_TOKEN = os.getenv('MANAGER_TOKEN')

subsidio_struct = {
    "tipoInput": "compliance/subsidios",
    "dados": [],
}


def get_standard_trip_number():
    standard_trips = [ # viagens no consorcio transnit
        {
            "totalViagens": 115685,
            "data": 1730419200000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 38928,
            "data": 1730505600000,
            "tipoDia": "Feriado"
        },
        {
            "totalViagens": 26077,
            "data": 1730592000000,
            "tipoDia": "Domingo"
        },
        {
            "totalViagens": 126530,
            "data": 1730678400000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 135085,
            "data": 1730764800000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 132477,
            "data": 1730851200000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 133825,
            "data": 1730937600000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 123410,
            "data": 1731024000000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 50698,
            "data": 1731110400000,
            "tipoDia": "Sábado"
        },
        {
            "totalViagens": 24268,
            "data": 1731196800000,
            "tipoDia": "Domingo"
        },
        {
            "totalViagens": 129262,
            "data": 1731283200000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 132589,
            "data": 1731369600000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 108967,
            "data": 1731456000000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 131161,
            "data": 1731542400000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 31538,
            "data": 1731628800000,
            "tipoDia": "Feriado"
        },
        {
            "totalViagens": 39668,
            "data": 1731715200000,
            "tipoDia": "Sábado"
        },
        {
            "totalViagens": 23422,
            "data": 1731801600000,
            "tipoDia": "Domingo"
        },
        {
            "totalViagens": 114290,
            "data": 1731888000000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 116456,
            "data": 1731974400000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 32612,
            "data": 1732060800000,
            "tipoDia": "Feriado"
        },
        {
            "totalViagens": 124006,
            "data": 1732147200000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 114882,
            "data": 1732233600000,
            "tipoDia": "Feriado"
        },
        {
            "totalViagens": 43931,
            "data": 1732320000000,
            "tipoDia": "Sábado"
        },
        {
            "totalViagens": 20363,
            "data": 1732406400000,
            "tipoDia": "Domingo"
        },
        {
            "totalViagens": 121339,
            "data": 1732492800000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 124180,
            "data": 1732579200000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 125001,
            "data": 1732665600000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 122591,
            "data": 1732752000000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 115971,
            "data": 1732838400000,
            "tipoDia": "Útil"
        },
        {
            "totalViagens": 49725,
            "data": 1732924800000,
            "tipoDia": "Sábado"
        }
    ]
    
    df_viagens = pd.DataFrame.from_dict(standard_trips)
    soma_viagens = df_viagens['totalViagens'].sum().item()
    return soma_viagens

def calcular_subsidio(compliance):

    if compliance > 100 or (100 >= compliance and compliance >= 95):
        return 100
    if 94 >= compliance and compliance >= 90:
        return 95
    if 89 >= compliance and compliance >= 85:
        return 85
    if 84 >= compliance and compliance >= 80:
        return 70
    return 0
    # Escala                  Subsídio a
    # de Cumprimento(%)       Receber (%)
    # 100-95                      100
    # 94-90                       95
    # 89-85                       85
    # 84-80                       70
    # <80                         0


def viagem_programada(inicio, fim, empresa, linha):
    # Item 1- Viagem programada x realizada
    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/dados-operacionais/viagens/qtd-viagens-dia?Linhas={linha}&from={inicio}&to={fim}&Empresas={empresa}"
    response = requests.get(url).json()
    df_viagens = pd.DataFrame.from_dict(response['dados'])
    soma_viagens = df_viagens['totalViagens'].sum().item()
    meta_viagens = get_standard_trip_number() # no futuro, substituir pela meta real de viagens
    compliance_viagens = (soma_viagens/meta_viagens)*100
    subsidio_concedido = calcular_subsidio(compliance_viagens)
    # subsidios_totais(subsidio_struct['dados'], 'bus_trips', compliance_viagens, subsidio_concedido)
    payload = {
        "tipoInput": "compliance/numero_viagens",
        "dados": {
            "consorcio": "TransNit",
            "viagensRealizadas": soma_viagens,
            "compliance": compliance_viagens,
            "porcentagem_conclusao": compliance_viagens,
            "subsidio_concedido": subsidio_concedido
        }
    }
    return payload

    response_binario = json.dumps(payload, indent=2).encode('utf-8')
    return response_binario


def bus_km_compliance(linhas, treshold, inicio, fim):
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
    subsidio_concedido = calcular_subsidio(compliance_km * 100)

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
    return payload

    # Transforma response em Binário para enviar ao dApp
    response_binario = json.dumps(payload, indent=2).encode('utf-8')
    return response_binario


def climatizacao(empresa):
    # Item 3- Climatização das frotas

    compliance_climatizacao = get_consortium_compliance(empresa)
    subsidio_concedido = calcular_subsidio(compliance_climatizacao)
    # subsidios_totais(subsidio_struct['dados'], 'bus_ac', compliance_climatizacao, subsidio_concedido)
    payload = {
        "tipoInput": "compliance/climatizacao",
        "dados": {
            "consorcio": 'TransNit',
            "compliance": compliance_climatizacao,
            "porcentagem_conclusao": compliance_climatizacao,
            "subsidio_concedido": subsidio_concedido
        }
    }
    return payload

    response_binario = json.dumps(payload, indent=2).encode('utf-8')
    return response_binario

def bus_amount_compliance(inicio, fim, empresas):
    # Item 4- Quantidade de ônibus programada x realizada

    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/indicadores/frota/disponivel-programada?Threshold={treshold}&from={inicio}&to={fim}&Empresas={empresas}"

    response = requests.get(url).json()

    dados_onibus_df = pd.DataFrame.from_dict(response['dados'])

    # Calcula total de frotas programadas e disponíveis
    frota_programada = dados_onibus_df['frotaProgramada'].sum()
    frota_disponivel = dados_onibus_df['frotaDisponivel'].sum()

    # Cria novo DataFrame com os totais por Consórcio
    dados_onibus_df = pd.DataFrame({'total_frotas_programadas': [frota_programada], 'total_frotas_disponiveis': [frota_disponivel]})

    # Calcula a porcentagem da Escala de Cumprimento
    compliance_frota = round((frota_disponivel / frota_programada), 2)

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
    return payload

    # Transforma response em Binário para enviar ao dApp
    response_binario = json.dumps(payload, indent=2).encode('utf-8')
    return response_binario


# def subsidios_totais(dados, nome_compliance, valor_compliance, subsidio_concedido):

#     dados.append(
#         {
#             "nome_compliance": nome_compliance,
#             "valor_compliance": valor_compliance,
#             "total_subsidio": subsidio_concedido
#         }
#     )

#     return 0


def envia_input_dapp(payload):
    # Conexão com a rede Ethereum
    ## Conecta à rede Foundry para interagir com o dApp
    DAPP_ADDRESS = os.getenv('DAPP_ADDRESS')

    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    if w3.isConnected:
        print("conectado")

    # Busca os dados do Contrato que usaremos para enviar Inputs para o dApp (InputBox)
    INPUT_BOX_ADDRESS = os.getenv('INPUT_BOX_ADDRESS')
    abi = '[ { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "inputLength", "type": "uint256" }, { "internalType": "uint256", "name": "maxInputLength", "type": "uint256" } ], "name": "InputTooLarge", "type": "error" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "appContract", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "index", "type": "uint256" }, { "indexed": false, "internalType": "bytes", "name": "input", "type": "bytes" } ], "name": "InputAdded", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "bytes", "name": "payload", "type": "bytes" } ], "name": "addInput", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "getInputHash", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" } ], "name": "getNumberOfInputs", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" } ]'
    contract_instance = w3.eth.contract(address=INPUT_BOX_ADDRESS, abi=abi)

    # Cria e executa a transação para a rede
    transaction = contract_instance.functions.addInput(DAPP_ADDRESS, payload).transact()
    print(transaction)

    return transaction

if __name__ == '__main__':

    # Parâmetros para as requisições
    linhas = f"%2735%27%2C%2734A%27"
    treshold = f"%270%27"
    inicio = f"1727740800000"
    fim = "1730419199999"
    empresas = 'INGÁ'
    consorcio = "TRANSNIT"

    # Item 1- Quilometragem Programada
    response_viagens_programadas = viagem_programada(inicio, fim, empresas, linhas)
    # envia_input_dapp(response_viagens_programadas)
    print('\n', response_viagens_programadas)
    # Item 2- Quilometragem Programada
    response_km_programada = bus_km_compliance(linhas, treshold, inicio, fim)
    # envia_input_dapp(response_km_programada)
    print('\n', response_km_programada)
    # Item 3 - Climatização da Frota
    response_climatizacao = climatizacao(consorcio)
    # envia_input_dapp(response_climatizacao)
    print('\n', response_climatizacao)
    # Item 4- Quantidade de Ônibus
    response_frota_disponivel = bus_amount_compliance(inicio, fim, empresas)
    # envia_input_dapp(response_frota_disponivel)
    print('\n', response_frota_disponivel)
    # Subsídios Totais
    # struct_json = json.dumps(subsidio_struct, indent=2).encode('utf-8')
    # envia_input_dapp(struct_json)