import requests
import pandas as pd
import json
from eth_abi import encode_abi
from eth_utils import function_signature_to_4byte_selector
from web3 import Web3, EthereumTesterProvider

MOBNIT_API_URL = "https://mobnit.niteroi.rj.gov.br/api/website/v1"
MANAGER_TOKEN = "qkiybj2rx8rwnn6cnhyweiwx6bt1kq5e"

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


def quantidade_onibus(inicio, fim, empresas):
    # Item 4- Quantidade de ônibus programada
    treshold = f"%270%27"
    inicio = f"1727740800000"
    fim = "1730419199999"
    url = f"{MOBNIT_API_URL}/dados/{MANAGER_TOKEN}/indicadores/frota/disponivel-programada?Threshold={treshold}&from={inicio}&to={fim}&Empresas={empresas}"

    response = requests.get(url).json()

    return response

if __name__ == '__main__':
    linhas = f"%2735%27%2C%2734A%27"
    inicio = "1727740800000"
    fim = "1730419199999"
    empresas = 'Transportes Peixoto Ltda'

    response = quantidade_onibus(inicio, fim, empresas)
    dados_onibus_df = pd.DataFrame.from_dict(response['dados'])
    print(dados_onibus_df)
    compliance_frota = dados_onibus_df['frotaDisponivel'].sum() / dados_onibus_df['frotaProgramada'].sum()
    print(compliance_frota)
    response['complianceSubsidio'] = "%.2f" % (compliance_frota * 100) 

    response_binario = json.dumps(response, indent=2).encode('utf-8')

    DAPP_ADDRESS = "0xab7528bb862fB57E8A2BCd567a2e929a0Be56a5e"

    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    if w3.isConnected:
        print("conectado")

    inputBoxAddress = '0x59b22D57D4f067708AB0c00552767405926dc768'
    abi = '[ { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "inputLength", "type": "uint256" }, { "internalType": "uint256", "name": "maxInputLength", "type": "uint256" } ], "name": "InputTooLarge", "type": "error" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "appContract", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "index", "type": "uint256" }, { "indexed": false, "internalType": "bytes", "name": "input", "type": "bytes" } ], "name": "InputAdded", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "bytes", "name": "payload", "type": "bytes" } ], "name": "addInput", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "getInputHash", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" } ], "name": "getNumberOfInputs", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" } ]'
    
    contract_instance = w3.eth.contract(address=inputBoxAddress, abi=abi)
    transaction = contract_instance.functions.addInput(DAPP_ADDRESS, response_binario).transact()
    print(transaction)
    
    # Escala                  Subsídio a
    # de Cumprimento(%)       Receber (%)
    # 100-95                      100
    # 94-90                       95
    # 89-85                       85
    # 84-80                       70
    # <80                         0
