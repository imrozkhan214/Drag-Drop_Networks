import socket
import os
import ssl

# Set up the server to accept connections securely
def start_server(host, port):
    # Create SSL context for server-side authentication
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")  # Add your server certificate and key
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    secure_server_socket = context.wrap_socket(server_socket, server_side=True)
    return secure_server_socket

# Handle a client connection and save the file sent by the client
def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        
        # If it's a file transfer request
        if data.startswith("FILE:"):
            file_size = int(data.split(":")[1])
            with open("received_file", "wb") as file:
                while file_size > 0:
                    chunk = client_socket.recv(min(file_size, 1024))
                    file.write(chunk)
                    file_size -= len(chunk)
            print("File received successfully.")
        else:
            print("Invalid data received.")

    except Exception as e:
        print(f"Error receiving file: {e}")

    finally:
        # Close the connection after processing the file
        client_socket.close()

# Main function to listen for incoming connections and handle file transfers
def main():
    host = "localhost"  # The server's IP address
    port = 12345  # The server's port

    # Start the server
    server_socket = start_server(host, port)

    # Accept client connections and handle them
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
