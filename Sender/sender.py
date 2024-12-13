import tkinter as tk
from tkinter import filedialog
import socket
import os

def send_file():
    file_path = entry.get()
    host = host_entry.get()
    port = port_entry.get()

    if file_path and host and port:
        try:
            # Convert the port to an integer
            port = int(port)
            
            # Open the file and prepare to send
            with open(file_path, 'rb') as f:
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)  # Get the file size
                
                # Create socket connection to the receiver
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))

                # Send the filename and file size first
                filename_bytes = filename.encode()  # Convert filename to bytes
                client_socket.send(len(filename_bytes).to_bytes(4, byteorder='big'))  # Send length of filename
                client_socket.send(filename_bytes)  # Send filename as bytes
                client_socket.send(file_size.to_bytes(8, byteorder='big'))  # Send file size as bytes

                # Send the file data in chunks
                file_data = f.read(1024)
                while file_data:
                    client_socket.send(file_data)
                    file_data = f.read(1024)

                print("File sent successfully!")
                client_socket.close()

        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Please fill in all fields.")

def browse_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Create the Tkinter window
root = tk.Tk()
root.title("File Sender")
root.geometry("500x350")  # Set the window size (width x height)
root.resizable(False, False)  # Disable window resizing

# Create a Frame for better control over widget placement
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

label = tk.Label(frame, text="Select a file to send:", font=('Arial', 14), anchor='w')
label.grid(row=0, column=0, pady=10, sticky="w")

entry = tk.Entry(frame, width=40, font=('Arial', 12))
entry.grid(row=1, column=0, padx=10, pady=10)

button_browse = tk.Button(frame, text="Browse", command=browse_file, font=('Arial', 12), width=15)
button_browse.grid(row=2, column=0, pady=10)

# Host input field
host_label = tk.Label(frame, text="Host (Receiver's IP):", font=('Arial', 12))
host_label.grid(row=3, column=0, pady=5, sticky="w")
host_entry = tk.Entry(frame, width=40, font=('Arial', 12))
host_entry.grid(row=4, column=0, padx=10, pady=5)

# Port input field
port_label = tk.Label(frame, text="Port:", font=('Arial', 12))
port_label.grid(row=5, column=0, pady=5, sticky="w")
port_entry = tk.Entry(frame, width=40, font=('Arial', 12))
port_entry.grid(row=6, column=0, padx=10, pady=5)

button_send = tk.Button(frame, text="Send File", command=send_file, font=('Arial', 12), width=15)
button_send.grid(row=7, column=0, pady=10)

root.mainloop()
