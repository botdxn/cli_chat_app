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
                threading.Thread(target=conn_handler, args=[sock_conn, address]).start()

        # Handle errors
        except Exception as e:
            sys.stdout.write(f"Exception: {e}")
            pass

        # Wipe connections and close server in case of problems
        finally:
            if len(GLOB_CONNECTIONS) > 0:
                for conn in GLOB_CONNECTIONS:
                    del_conn(conn)

            sock.close()


if __name__ == "__main__":
    t = Server(12000)
    t.server_handler()
