import pandas as pd
import json
import os
import locale
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv
from get_from_excel import get_consortium_compliance
from api_sql import *

load_dotenv()

MOBNIT_API_URL = os.getenv("MOBNIT_API_URL")
MANAGER_TOKEN = os.getenv("MANAGER_TOKEN")
PRIVATE_KEY= os.environ.get('PRIVATE_KEY')

# METAS DE NUMERO DE VIAGENS - AMBAS OBTIDAS DO MÊS DE SETEMBRO DE 2024
META_VIAGENS_TRANSNIT = 2823858
META_VIAGENS_TRANSOCEANICO = 3847979

def calcular_subsidio(compliance):
    if compliance > 100 or (100 >= compliance and compliance >= 95):
        return 100
    if 94 >= compliance and compliance > 90:
        return 95
    if 90 >= compliance and compliance > 85:
        return 85
    if 85 >= compliance and compliance >= 80:
        return 70
    return 0
    # Escala                  Subsídio a
    # de Cumprimento(%)       Receber (%)
    # 100-95                      100
    # 94-90                       95
    # 89-85                       85
    # 84-80                       70
    # <80                         0


def viagem_programada(consorcio):
    response = get_from_api(consorcio, "viagens")
    df_viagens = pd.DataFrame.from_dict(response)
    soma_viagens = df_viagens["totalViagens"].sum().item()
    meta_viagens = (
        META_VIAGENS_TRANSNIT if consorcio == "transnit" else META_VIAGENS_TRANSOCEANICO
    )
    compliance_viagens = round(((soma_viagens / meta_viagens) * 100), 2)

    subsidio_concedido = calcular_subsidio(compliance_viagens)

    payload = {
        "tipoInput": "compliance/numero_viagens",
        "dados": {
            "consorcio": consorcio,
            "viagensRealizadas": soma_viagens,
            "compliance": {
                "meta_viagens_realizadas": meta_viagens,
                "total_viagens_realizadas": soma_viagens,
            },
            "porcentagem_conclusao": compliance_viagens,
            "subsidio_concedido": subsidio_concedido,
        },
    }
    return payload


def bus_km_compliance(consorcio):
    # Item 2- Quilometragem programada x realizada

    # Ida
    response_ida = get_from_api(consorcio, "quilometragem-ida")
    df_ida = pd.DataFrame.from_dict(response_ida)

    # Volta
    response_volta = get_from_api(consorcio, "quilometragem-volta")
    df_volta = pd.DataFrame.from_dict(response_volta)

    # Merge Ida e Volta em 'numeroLinha'
    df_totais = pd.merge(
        df_ida, df_volta, on="numeroLinha", suffixes=("_ida", "_volta")
    )

    # Calcula total_programada e total_realizada
    total_programada = round(
        (df_totais["kmProgramadaIda"] + df_totais["kmProgramadaVolta"]).sum().item(), 2
    )
    total_realizada = round(
        (df_totais["kmRealizadaIda"] + df_totais["kmRealizadaVolta"]).sum().item(), 2
    )

    # Cria novo DataFrame com os totais por Consórcio
    dados_km_json = {
        "total_programada": total_programada,
        "total_realizada": total_realizada,
    }

    # Calcula a porcentagem da Escala de Cumprimento
    compliance_km = round((total_realizada / total_programada), 2) * 100
    subsidio_concedido = calcular_subsidio(compliance_km)

    payload = {
        "tipoInput": "compliance/quilometragem_percorrida",
        "dados": {
            "consorcio": consorcio,
            "compliance": dados_km_json,
            "porcentagem_conclusao": compliance_km,
            "subsidio_concedido": subsidio_concedido,
        },
    }
    return payload


def climatizacao(consorcio: str):
    # Item 3- Climatização das frotas

    compliance_climatizacao, total_onibus, nao_climatizados = get_consortium_compliance(
        consorcio.upper()
    )

    compliance_climatizacao = round(compliance_climatizacao, 2)
    subsidio_concedido = calcular_subsidio(compliance_climatizacao)

    payload = {
        "tipoInput": "compliance/climatizacao",
        "dados": {
            "consorcio": consorcio,
            "compliance": {
                "total_onibus": total_onibus,
                "nao_climatizados": nao_climatizados,
            },
            "porcentagem_conclusao": compliance_climatizacao,
            "subsidio_concedido": subsidio_concedido,
        },
    }
    return payload


def bus_amount_compliance(consorcio):
    # Item 4- Quantidade de ônibus programada x realizada

    response = get_from_api(consorcio, "frota")

    dados_onibus_df = pd.DataFrame.from_dict(response)

    # Calcula total de frotas programadas e disponíveis
    frota_programada = dados_onibus_df["frotaProgramada"].sum()
    frota_disponivel = dados_onibus_df["frotaDisponivel"].sum()

    # Cria novo DataFrame com os totais por Consórcio
    dados_onibus_json = {
        "total_frotas_programadas": frota_programada,
        "total_frotas_disponiveis": frota_disponivel,
    }

    # Calcula a porcentagem da Escala de Cumprimento
    compliance_frota = round((frota_disponivel / frota_programada) * 100, 2)

    # Calcula a porcentagem do Subsídio
    subsidio_concedido = calcular_subsidio(compliance_frota)

    payload = {
        "tipoInput": "compliance/frota_disponivel",
        "dados": {
            "consorcio": consorcio,
            "compliance": dados_onibus_json,
            "porcentagem_conclusao": compliance_frota,
            "subsidio_concedido": subsidio_concedido,
        },
    }
    return payload


def envia_input_dapp(payload):
    # Conexão com a rede Ethereum
    ## Conecta à rede Foundry para interagir com o dApp
    DAPP_ADDRESS = os.getenv("DAPP_ADDRESS")

    w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/FJ7ZicZFKOFpDMTAiYjyLV-9t-lVjsa7"))

    # Busca os dados do Contrato que usaremos para enviar Inputs para o dApp (InputBox)
    INPUT_BOX_ADDRESS = os.getenv("INPUT_BOX_ADDRESS")
    abi = '[ { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "inputLength", "type": "uint256" }, { "internalType": "uint256", "name": "maxInputLength", "type": "uint256" } ], "name": "InputTooLarge", "type": "error" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "appContract", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "index", "type": "uint256" }, { "indexed": false, "internalType": "bytes", "name": "input", "type": "bytes" } ], "name": "InputAdded", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "bytes", "name": "payload", "type": "bytes" } ], "name": "addInput", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" }, { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "getInputHash", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "appContract", "type": "address" } ], "name": "getNumberOfInputs", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" } ]'
    contract_instance = w3.eth.contract(address=INPUT_BOX_ADDRESS, abi=abi)
    wallet = w3.eth.account.from_key(PRIVATE_KEY)
    # Cria e executa a transação para a rede
    payload_binario = json.dumps(payload, indent=2).encode("utf-8")
    transaction = contract_instance.functions.addInput(
        DAPP_ADDRESS, payload_binario
    ).build_transaction({
        "from": wallet.address,
        "nonce": w3.eth.get_transaction_count(wallet.address)
    })
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=wallet.key)
    tx_result = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_result)

    return transaction

def get_consortium_subsidy_data(consorcio):
    
    response_viagens_programadas = viagem_programada(consorcio)
    print("\n", response_viagens_programadas)

    # Item 2- Quilometragem Programada
    response_km_programada = bus_km_compliance(consorcio)
    print("\n", response_km_programada)

    # Item 3 - Climatização da Frota
    response_climatizacao = climatizacao(consorcio)
    print("\n", response_climatizacao)

    # Item 4- Quantidade de Ônibus
    response_frota_disponivel = bus_amount_compliance(consorcio)
    print("\n", response_frota_disponivel)

    subsidio_total = (
        response_viagens_programadas["dados"]["subsidio_concedido"]
        + response_km_programada["dados"]["subsidio_concedido"]
        + response_climatizacao["dados"]["subsidio_concedido"]
        + response_frota_disponivel["dados"]["subsidio_concedido"]
    ) / 4

    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

    today = datetime.date.today().replace(day=1)
    data_aferida = (today - datetime.timedelta(days=1)).strftime("%B/%Y")

    payload = {
        "tipoInput": "compliance/subsidios",
        "consorcio": consorcio,
        "subsidio_total": subsidio_total,
        "data_aferida": data_aferida,
        "dados": [
            response_viagens_programadas,
            response_km_programada,
            response_climatizacao,
            response_frota_disponivel,
        ],
    }

    return payload

def lambda_handler(event, context):
    payload_transnit = get_consortium_subsidy_data('transnit')
    payload_transoceanico = get_consortium_subsidy_data('transoceânico')
    envia_input_dapp(payload_transnit)
    envia_input_dapp(payload_transoceanico)
    return True
