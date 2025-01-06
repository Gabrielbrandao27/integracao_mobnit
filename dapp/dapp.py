from os import environ
import logging
import requests
import db_manager as db
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
db_getter = db.DBConnector()
rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]

logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")


def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


bus_data = []

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    conn = db_getter.create_connection('integracao_mobnit.db')

    payload = hex2str(data["payload"])
    logger.info(f"Payload: {payload}")
    payload_json = json.loads(payload)

    for info_linha in payload_json['dados']:
        logger.info(f"Info linha: {info_linha}")
        logger.info(f"Linha: {info_linha['linha']}")
        if not db.insert_bus_line(conn, info_linha['linha']):
            return "reject"
        
    lines_query_result = db.select_lines(conn)
    logger.info(f"Lines query result: {lines_query_result}")

    match payload_json['tipoInput']:
        case 'compliance/frota':
            for info_linha in payload_json['dados']:
                if not db.insert_compliance_data(conn, info_linha):
                    return "reject"
        case _:
            logger.info("Unknown type of input")
            return "reject"
    

    # for id in lines_query_result:
    #     compliance_query_result = db.select_compliance_data(conn, )

    return "accept"


def handle_inspect(data):
    logger.info(f"Received Brandão e Marcelo inspect request data {data}")

    report = {
        "payload": str2hex(
            f"{bus_data}"
        )
    }

    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
