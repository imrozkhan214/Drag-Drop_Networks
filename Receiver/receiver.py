import socket

def receive_file():
    host = '127.0.0.1'  # Localhost (or you can use an IP address of the receiver machine)
    port = 10760         # Port number for the connection

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for 1 connection at a time

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Receive the file name
    filename = client_socket.recv(1024).decode()
    print(f"Receiving file: {filename}")

    # Receive the file content in chunks and save it
    with open(filename, 'wb') as f:
        while True:
            file_data = client_socket.recv(1024)
            if not file_data:
                break
            f.write(file_data)

    print(f"File {filename} received successfully!")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    receive_file()
