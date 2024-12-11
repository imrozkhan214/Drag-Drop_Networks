# protocol.py

# Simple handshake and file transfer protocol

def protocol_handshake(client_socket):
    # Client sends a greeting message
    client_socket.send("HELLO Server".encode())
    response = client_socket.recv(1024).decode()
    if response == "READY":
        print("Handshake successful.")
        return True
    else:
        print("Handshake failed.")
        return False

def protocol_file_transfer(client_socket, file_name, file_size):
    # Sending file metadata
    client_socket.send(f"FILE:{file_name}:{file_size}".encode())

def protocol_end_of_transfer(client_socket):
    # End transfer message
    client_socket.send("TRANSFER COMPLETE".encode())
    response = client_socket.recv(1024).decode()
    if response == "TRANSFER ACKNOWLEDGED":
        print("Transfer acknowledged by server.")
