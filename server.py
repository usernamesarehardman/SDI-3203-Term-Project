import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

HOST = "127.0.0.1"
PORT = 5555
clients = {}  # Maps client socket -> username

def broadcast(message, sender_socket=None):
    """Sends a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        del clients[client_socket]
    client_socket.close()

def handle_client(client_socket):
    """Handles communication with a single connected client."""
    try:
        username = client_socket.recv(1024).decode('utf-8')
        if username in clients.values():
            client_socket.send("Username already taken. Try again.".encode('utf-8'))
            client_socket.close()
            return

        clients[client_socket] = username
        logging.info(f"{username} joined the chat.")
        broadcast(f"{username} has joined the chat!")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.lower() == "server:exit":
                break

            # Handle direct messages: <recipient>:<message>
            if ':' in message:
                recipient, dm_message = message.split(':', 1)
                recipient = recipient.strip()
                dm_message = dm_message.strip()
                sent_dm = False
                for c, user in clients.items():
                    if user == recipient:
                        c.send(f"[DM from {username}] {dm_message}".encode('utf-8'))
                        sent_dm = True
                        break
                if not sent_dm:
                    client_socket.send("[SERVER] Recipient not found.".encode('utf-8'))
            else:
                # Broadcast to everyone else
                broadcast(f"{username}: {message}", client_socket)

    except Exception as e:
        logging.error(f"Exception in client handler: {e}")
    finally:
        user_left = clients.get(client_socket, "Unknown")
        remove_client(client_socket)
        broadcast(f"{user_left} has left the chat.")

def start_server():
    """Starts the server and listens for incoming client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        logging.info(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()