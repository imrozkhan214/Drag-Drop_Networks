import socket

def receive_file():
    host = '192.168.56.1'  # Localhost (or you can use an IP address of the receiver machine)
    port = 10760         # Port number for the connection

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for 1 connection at a time

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Receive the length of the filename
    filename_len = int.from_bytes(client_socket.recv(4), byteorder='big')  # Read the filename length
    filename = client_socket.recv(filename_len).decode('utf-8', 'ignore')  # Receive the filename as bytes
    print(f"Receiving file: {filename}")

    # Receive the file size as raw bytes (8 bytes for the file size)
    file_size = int.from_bytes(client_socket.recv(8), byteorder='big')  # Get the file size as an integer
    print(f"File size: {file_size} bytes")

    # Receive the file content in chunks and save it
    with open(filename, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            file_data = client_socket.recv(1024)
            if not file_data:
                break
            f.write(file_data)
            bytes_received += len(file_data)

    print(f"File {filename} received successfully!")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    receive_file()
