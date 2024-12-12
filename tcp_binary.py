import socket
import struct
import threading
import time

# Constants
HOST = '127.0.0.1'
PORT = 65432
MESSAGE_COUNT = 100

# Utility functions to send and receive messages using length-prefixed protocol
def send_message(conn, message):
    """Send a message with a length prefix."""
    message_length = len(message)
    conn.sendall(struct.pack('!I', message_length))  # Send 4-byte length prefix
    conn.sendall(message)  # Send the actual message

def receive_message(conn):
    """Receive a message with a length prefix."""
    length_prefix = conn.recv(4)
    if not length_prefix:
        return None
    message_length = struct.unpack('!I', length_prefix)[0]  # Unpack 4-byte length prefix
    return conn.recv(message_length)

# Server process
def server_process():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server: Waiting for a connection...")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Server: Connected by {addr}")
            for i in range(MESSAGE_COUNT):
                message = receive_message(conn)
                print(f"Server received: {message.decode()}")

                response = f"Message {i + 1} received!".encode()
                send_message(conn, response)

# Client process
def client_process():
    time.sleep(1)  # Ensure the server starts first
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Client: Connected to the server")
        for i in range(MESSAGE_COUNT):
            message = f"Hello, Server! This is message {i + 1}".encode()
            send_message(client_socket, message)
            print(f"Client sent: {message.decode()}")

            response = receive_message(client_socket)
            print(f"Client received: {response.decode()}")

# Start the server and client threads
server_thread = threading.Thread(target=server_process, daemon=True)
client_thread = threading.Thread(target=client_process, daemon=True)

server_thread.start()
client_thread.start()

# Wait for threads to complete
server_thread.join()
client_thread.join()

print("Communication completed.")
