import logging
import socket

from server import SERVER


def run_client():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        client.connect((SERVER.address, SERVER.port))
        logging.info("connected to {}:{}".format(SERVER.address, SERVER.port))

        while True:

            try:

                data_to_send = input(
                    "send to {}:{} > ".format(SERVER.address, SERVER.port)
                )
                client.sendall(data_to_send.encode())
                logging.info('message has been sent.')
                data = client.recv(1024)  # 1 byte
                if data:
                    logging.info(
                        "from {}:{} received > {}".format(SERVER.address, SERVER.port, data.decode('utf-8'))
                    )
            except KeyboardInterrupt:
                logging.info("connection has been closed")
                break
            except BrokenPipeError:
                logging.info("connection has been closed from {}:{}".format(SERVER.address, SERVER.port))
                break


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    run_client()
