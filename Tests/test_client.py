# test_client.py
import unittest
import socket
from Client import connect_to_server, send_file

class TestClient(unittest.TestCase):
    
    def test_connection(self):
        # Test connection to server
        client_socket = connect_to_server("localhost", 5000)
        self.assertIsNotNone(client_socket)
    
    def test_send_file(self):
        # Assuming there is a test file "test.txt"
        client_socket = connect_to_server("localhost", 5000)
        send_file("test.txt", client_socket)
        # If no exceptions are raised, the test passes
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
