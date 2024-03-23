import logging
from threading import Thread

from socket_server import run_socker_server
from http_server import run_http_server


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")

    socket_thread = Thread(target=run_socker_server)
    socket_thread.start()

    http_thread = Thread(target=run_http_server)
    http_thread.start()

    http_thread.join()
    socket_thread.join()
