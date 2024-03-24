import logging
import socket
from datetime import datetime
from urllib.parse import unquote_plus
from pymongo.mongo_client import MongoClient
from constants import BUFFER_SIZE, SOCKET_HOST, SOCKET_PORT

URI = "mongodb://mongoserver:27017"


def run_socker_server():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            logging.info(f"Socket server started on {SOCKET_HOST}:{SOCKET_PORT}")
            server_socket.bind((SOCKET_HOST, SOCKET_PORT))

            while True:
                data, addr = server_socket.recvfrom(BUFFER_SIZE)
                data_decoded = data.decode()
                logging.debug(f"Received message: {data_decoded} from {addr}")
                save_data(data_decoded)

    except Exception as e:
        logging.error(f"Socket server error: {e}")

    logging.info("Socket server stopped")


def save_data(data):
    parsed_data = parse_data(data)
    parsed_data["date"] = datetime.now()

    try:
        with MongoClient(URI) as client:
            db = client["messanger"]
            messages = db["messages"]
            messages.insert_one(parsed_data)
            logging.debug("Message saved successfully")
    except Exception as e:
        logging.error(f"Error while saving data: {e}")


def parse_data(data):
    try:
        unquoted_data = unquote_plus(data)
        parsed_data = {
            key: value
            for key, value in [el.split("=") for el in unquoted_data.split("&")]
        }
        return parsed_data
    except ValueError as e:
        logging.error(f"Error while parsing data: {e}")
        raise
