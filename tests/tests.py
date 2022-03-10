import unittest
from unittest.mock import Mock
from src.server_app import Server
from src.client_app import Client

class TestServer(unittest.TestCase):
    def test_server_class(self):
        test_port = 10000
        test_call = Server(test_port).server_handler()


if __name__ == "__main__":
    unittest.main()
