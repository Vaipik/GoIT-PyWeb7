import logging
import socket

from addresses import IPAddress


SERVER = IPAddress(address="127.0.0.1", port=5000)


def run_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # To use port immediate after restart
        server.bind((SERVER.address, SERVER.port))
        server.listen()

        conn, addr = server.accept()

        with conn:

            logging.info("connection from {}:{} accepted".format(*addr))
            while True:
                try:
                    received_data = conn.recv(1024)  # 1 byte
                    logging.info(
                        "from {}:{} received > {}".format(*addr, received_data.decode('utf-8'))
                    )
                    data_to_send = input(
                        "send to {}:{} > ".format(*addr)
                    )
                    conn.sendall(data_to_send.encode())
                    logging.info("message has been sent.")
                except KeyboardInterrupt:
                    logging.info(
                        "connection closed from {}:{}".format(SERVER.address, SERVER.port)
                    )
                    break
                except BrokenPipeError:
                    logging.info("connection has been closed from {}:{}".format(*addr))


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    run_server()
