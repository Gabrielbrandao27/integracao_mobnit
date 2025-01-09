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


def dataset_to_json(keys, dataset):
    # Define the keys based on the dataset structure
    json_list = [dict(zip(keys, row)) for row in dataset]
    return json.dumps(json_list)

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    conn = db_getter.create_connection('integracao_mobnit.db')

    payload = hex2str(data["payload"])
    logger.info(f"Payload: {payload}")
    payload_json = json.loads(payload)

    if payload_json['tipoInput'] == 'compliance/subsidios':
        if not db.insert_consorcium(conn, payload_json['consorcio']):
            return "reject"
        if not db.insert_total_subsidy_data(conn, payload_json['consorcio'], payload_json['subsidio_total']):
            return "reject"
        for item in payload_json['dados']:
            match item["tipoInput"]:
                case 'compliance/numero_viagens':
                    if not db.insert_bus_trip_compliance_data(conn, item):
                        return "reject"
                    bus_trip_compliance_query = db.select_bus_trip_compliance_data(conn)
                    logger.info(f"Bus trip compliance query result: {bus_trip_compliance_query}")

                case 'compliance/quilometragem_percorrida':
                    if not db.insert_bus_km_compliance_data(conn, item):
                        return "reject"
                    bus_km_compliance_query = db.select_bus_km_compliance_data(conn)
                    logger.info(f"Bus km compliance query result: {bus_km_compliance_query}")
                
                case 'compliance/climatizacao':
                    if not db.insert_bus_climatization_compliance_data(conn, item):
                        return "reject"
                    bus_climatization_compliance_query = db.select_bus_climatization_compliance_data(conn)
                    logger.info(f"Bus climatization compliance query result: {bus_climatization_compliance_query}")

                case 'compliance/frota_disponivel':
                    if not db.insert_bus_amount_compliance_data(conn, item):
                        return "reject"
                    bus_amount_compliance_query = db.select_bus_amount_compliance_data(conn)
                    logger.info(f"Bus amount compliance query result: {bus_amount_compliance_query}")

                case _:
                    logger.info("Unknown type of input")
                    return "reject"

    conn.close()

    return "accept"


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    
    conn = db_getter.create_connection('integracao_mobnit.db')
    
    payload = hex2str(data["payload"])
    logger.info(f"Payload: {payload}")

    match payload:
        case 'frotas_disponiveis':
            logger.info("Frotas disponíveis")
            bus_amount_compliance_query = db.select_bus_amount_compliance_data(conn)
            logger.info(f"Bus amount compliance query result: {bus_amount_compliance_query}")
            
            keys = ["id", "line_id", "expected_bus_amount", "recorded_bus_amount"]
            json_data = dataset_to_json(keys, bus_amount_compliance_query)
            report = {
                "payload": str2hex(
                    f"{json_data}"
                )
            }
        case 'quilometragem_percorrida':
            logger.info("Frotas disponíveis")
            bus_km_compliance_query = db.select_bus_km_compliance_data(conn)
            logger.info(f"Bus km compliance query result: {bus_km_compliance_query}")

            keys = ["id", "line_id", "expected_travel_distance_km", "recorded_travel_distance_km"]
            json_data = dataset_to_json(keys, bus_km_compliance_query)
            report = {
                "payload": str2hex(
                    f"{json_data}"
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
