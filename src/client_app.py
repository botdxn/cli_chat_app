import socket
import threading
import sys


class Client:
    def __init__(self, server_ip, server_port) -> None:
        self.server_ip = server_ip
        self.server_port = server_port

    def message_handler(self, connection: socket.socket) -> None:
        while True:
            try:
                # Listen for incoming messages
                message = connection.recv(1024)

                # If message is received then decode it
                # Else close connection because there could be an error
                # or there is no message at all
                if message:
                    sys.stdout.write(f"{message.decode()}\n")
                else:
                    conn.close()
                    raise "No message received or error while receiving message"
                    break

            except Exception as e:
                sys.stdout.write(f"{e}\n")
                break

    def client_handler(self) -> None:
        # Initialization of client socket
        # Trying to connect with host server
        try:
            sock = socket.socket()
            sock.connect((self.server_ip, self.server_port))

            threading.Thread(target=self.message_handler, args=[sock]).start()

            sys.stdout.write(f"Connected with: {self.server_ip}:{self.server_port}\n")

            while True:
                message = input()

                if message == "/quit":
                    print("Quitting")
                    break

                sock.send(message.encode())

        except Exception as e:
            sys.stdout.write(f"{e}\n")
            sock.close()


if __name__ == "__main__":
    t = Client("127.0.0.1", 12000)
    t.client_handler()
