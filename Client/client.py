import socket
import os
import ssl

# Establishing a secure connection to the server
def connect_to_server(host, port):
    # Create SSL context for server authentication
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    connection = socket.create_connection((host, port))
    secure_connection = context.wrap_socket(connection, server_hostname=host)
    return secure_connection

# Send file to the server
def send_file(file_path, server_socket):
    try:
        # Get the file size
        file_size = os.path.getsize(file_path)
        
        # Send file size information to the server
        server_socket.send(f"FILE:{file_size}".encode())

        # Open the file and send in chunks
        with open(file_path, "rb") as file:
            while chunk := file.read(1024):
                server_socket.send(chunk)
        
        print("File sent successfully.")

    except Exception as e:
        print(f"Error sending file: {e}")

# Main function to interact with the server
def main():
    host = "localhost"  # The server's IP address or hostname
    port = 12345  # The server's port

    # Connect to the server
    client_socket = connect_to_server(host, port)

    # Specify the file to send
    file_path = "path_to_your_file.pdf"  # Update this path with the file you want to send

    # Send the file
    send_file(file_path, client_socket)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()
