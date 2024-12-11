# test_server.py
import unittest
from Server import handle_client

class TestServer(unittest.TestCase):
    
    def test_handle_client(self):
        # Here we would ideally mock the client socket and test handle_client
        # Example test that just ensures no errors occur
        mock_client_socket = unittest.mock.Mock()
        mock_address = ("localhost", 5000)
        handle_client(mock_client_socket, mock_address)
        # No errors means success
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
