import socket
import ssl
import os

# Handle incoming file from the client
def handle_client_connection(client_socket):
    try:
        # Receive the file size first
        data = client_socket.recv(1024).decode()
        if data.startswith("FILE:"):
            file_size = int(data.split(":")[1])

            # Prepare to receive the file
            with open("received_file", "wb") as f:
                received = 0
                while received < file_size:
                    chunk = client_socket.recv(1024)
                    f.write(chunk)
                    received += len(chunk)
                print(f"File received. Total size: {file_size} bytes")
        else:
            print("Invalid data received.")
        client_socket.close()
    except Exception as e:
        print(f"Error in handle_client_connection: {e}")
        client_socket.close()

def start_server(host, port):
    try:
        # Create a socket and bind it to the server's address
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))

        # Start listening for incoming connections
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        # Wrap the server socket with SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")  # Add your cert and key here
        server_socket = context.wrap_socket(server_socket, server_side=True)

        while True:
            # Accept an incoming connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Handle the client connection
            handle_client_connection(client_socket)

    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    # Start the server
    start_server('localhost', 5000)
