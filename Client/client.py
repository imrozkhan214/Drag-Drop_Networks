from flask import Flask, request, jsonify
import socket
import ssl
import os

app = Flask(__name__)

# Function to send a file to the server using custom protocol
def send_file_to_server(file_path):
    try:
        host = 'localhost'  # Change this to your server's IP if needed
        port = 5000  # Port on which the server is running
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # Create a socket and wrap it with SSL
        s = socket.create_connection((host, port))
        secure_socket = context.wrap_socket(s, server_hostname=host)

        # Send file size first
        file_size = os.path.getsize(file_path)
        secure_socket.send(f"FILE:{file_size}".encode())

        # Send the file in chunks
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                secure_socket.send(chunk)

        print("File sent successfully.")
        secure_socket.close()

    except Exception as e:
        print(f"Error sending file: {e}")

# Route for the file upload form
@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>File Transfer</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload File</button>
        </form>
    </body>
    </html>
    '''

# Route to handle file upload and trigger file transfer
@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file temporarily
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Call the function to send the file to the server
    send_file_to_server(file_path)

    return jsonify({"message": "File uploaded and sent to server successfully!"})

if __name__ == "__main__":
    # Ensure the uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
