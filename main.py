from multiprocessing import Process

from socket_server import run_socker_server
from http_server import run_http_server


if __name__ == "__main__":
    socket_process = Process(target=run_socker_server)
    socket_process.start()

    http_process = Process(target=run_http_server)
    http_process.start()

    http_process.join()
    socket_process.join()
