import tkinter as tk
from tkinter import filedialog
import socket
import os

def send_file():
    file_path = entry.get()
    if file_path:
        try:
            # Open the file and prepare to send
            with open(file_path, 'rb') as f:
                filename = os.path.basename(file_path)
                file_data = f.read(1024)

                # Create socket connection to the receiver
                host = '127.0.0.1'  # IP address of the receiver
                port = 10760        # Port number (must be the same as receiver)
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))

                # Send the filename first
                client_socket.send(filename.encode())

                # Send the file data in chunks
                while file_data:
                    client_socket.send(file_data)
                    file_data = f.read(1024)

                print("File sent successfully!")
                client_socket.close()

        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Please select a file.")

def browse_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Create the Tkinter window
root = tk.Tk()
root.title("File Sender")

label = tk.Label(root, text="Select a file to send:")
label.pack(pady=20)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.pack(pady=10)

button_send = tk.Button(root, text="Send File", command=send_file)
button_send.pack(pady=10)

root.mainloop()
