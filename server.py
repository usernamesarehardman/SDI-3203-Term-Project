import socket
import threading
import logging

# Configure logging
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
            if message.lower() == "server:exit":
                break
            elif message.lower() == "server:who":
                user_list = ", ".join(clients.values())
                client_socket.send(f"Active Users: {user_list}".encode('utf-8'))
            elif ':' in message:
                target_name, msg = message.split(':', 1)
                target_name = target_name.strip()
                msg = msg.strip()

                # Send message only to the target user
                found = False
                for sock, user in clients.items():
                    if user.lower() == target_name.lower():
                        sock.send(f"{username}: {msg}".encode('utf-8'))
                        found = True
                        break
                if not found:
                    client_socket.send(f"[SERVER] User '{target_name}' not found.".encode('utf-8'))
            else:
                client_socket.send("[SERVER] Invalid message format. Use <recipient>:<message>".encode('utf-8'))

    except Exception as e:
        logging.error(f"Exception in client handler: {e}")

    finally:
        remove_client(client_socket)

def remove_client(client_socket):
    """Removes a disconnected client from the clients dictionary."""
    if client_socket in clients:
        username = clients[client_socket]
        logging.info(f"{username} left the chat.")
        broadcast(f"{username} has left the chat.")
        del clients[client_socket]
        client_socket.close()

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
