# test_protocol.py
import unittest
from Protocol import protocol_handshake, protocol_file_transfer, protocol_end_of_transfer

class TestProtocol(unittest.TestCase):
    
    def test_handshake(self):
        # Assume we have a mock client socket
        mock_client_socket = unittest.mock.Mock()
        mock_client_socket.recv.return_value = "READY".encode()  # Mock server response
        result = protocol_handshake(mock_client_socket)
        self.assertTrue(result)

    def test_file_transfer(self):
        # Mock sending file metadata
        mock_client_socket = unittest.mock.Mock()
        protocol_file_transfer(mock_client_socket, "test.txt", 1024)
        mock_client_socket.send.assert_called_with("FILE:test.txt:1024".encode())
    
    def test_end_of_transfer(self):
        # Mock end-of-transfer protocol
        mock_client_socket = unittest.mock.Mock()
        protocol_end_of_transfer(mock_client_socket)
        mock_client_socket.send.assert_called_with("TRANSFER COMPLETE".encode())

if __name__ == "__main__":
    unittest.main()
