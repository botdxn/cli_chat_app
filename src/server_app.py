import socket
import threading
import sys


GLOB_CONNECTIONS = list()


class Server:
    def __init__(self, port) -> None:
        self.port = port

    def server_handler(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("", self.port))

            # How many max connections to listen for
            sock.listen(2)

            # Using standard-out write because I want the 'server running'
            # to appear on future logs.
            # Print will not (most likely) appear on logs.
            sys.stdout.write(f"Server running on PORT: {self.port}\n")
            print("Press [CTRL+BREAK] to exit (windows-only)")

            # Perma loop to listen for incoming connections
            while True:
                sock_conn, address = sock.accept()
                GLOB_CONNECTIONS.append(sock_conn)

                # Start new thread (instance) for incoming connection
                threading.Thread(
                    target=self.conn_handler, args=[sock_conn, address]
                ).start()

        # Handle errors
        except Exception as e:
            sys.stdout.write(f"Exception: {e}")
            pass

        # Wipe connections and close server in case of problems
        finally:
            if len(GLOB_CONNECTIONS) > 0:
                for conn in GLOB_CONNECTIONS:
                    self.terminate_connection(conn)

            sock.close()

    def conn_handler(self, connection: socket.socket, address: str) -> None:
        while True:
            try:
                message = connection.recv(1024)

                if message:
                    sys.stdout.write(
                        f"[{address[0]}:{address[1]}]: {message.decode()}\n"
                    )
                    message_to_broadcast = (
                        f"Recv from [{address[0]}:{address[1]}]: {message.decode()}"
                    )

                    self.broadcast_message(message_to_broadcast, connection)

                else:
                    self.terminate_connection(connection)

            except Exception as e:
                sys.stdout.write(f"{e}\n")
                self.terminate_connection(connection)
                break

    def broadcast_message(self, message: str, connection: socket.socket) -> None:
        for client in GLOB_CONNECTIONS:
            if client != connection:
                try:
                    client.send(message.encode())
                except Exception as e:
                    sys.stdout.write(f"{e}\n")
                    self.terminate_connection()

    def terminate_connection(self, connection: socket.socket) -> None:
        if connection in GLOB_CONNECTIONS:
            connection.close()
            GLOB_CONNECTIONS.remove(connection)


if __name__ == "__main__":
    t = Server(12000)
    t.server_handler()
