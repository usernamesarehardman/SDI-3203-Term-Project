import socket
import threading
import logging

# Configuration
HOST = "127.0.0.1"
PORT = 5555
MAX_MESSAGE_SIZE = 1024
clients = {}  # Maps client socket -> username

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def broadcast(message, sender_socket=None):
    """Sends a message to all clients except the sender."""
    for client in list(clients):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                logging.error("[SERVER] Error sending message to %s: %s", clients.get(client, "unknown"), e)
                remove_client(client)

def remove_client(client_socket):
    """Removes a client and closes its connection."""
    if client_socket in clients:
        username = clients[client_socket]
        del clients[client_socket]
        client_socket.close()
        logging.info("[SERVER] %s has been disconnected and removed.", username)

def parse_message(raw_message):
    """Parses a raw message into recipient and content, if formatted as a direct message."""
    if ':' not in raw_message:
        return None, None
    recipient, msg = raw_message.split(':', 1)
    return recipient.strip(), msg.strip()

def handle_client(client_socket):
    """Handles communication with a single connected client."""
    try:
        registration_message = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8').strip()

        if not registration_message.startswith("server:register "):
            client_socket.send("Invalid registration format. Use 'server:register <username>'.".encode('utf-8'))
            client_socket.close()
            return

        username = registration_message.split(" ", 1)[1].strip()
        if not username or username in clients.values():
            client_socket.send("Username already taken or invalid. Try again.".encode('utf-8'))
            client_socket.close()
            return


        clients[client_socket] = username
        logging.info("[SERVER] %s joined the chat.", username)
        broadcast(f"[SERVER] {username} has joined the chat!")

        while True:
            message = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8')
            if not message:
                break

            command = message.lower()
            if command == "server:exit":
                break
            elif command == "server:who":
                user_list = ", ".join(clients.values())
                client_socket.send(f"[SERVER] Active Users: {user_list}".encode('utf-8'))
            elif command == "server:help":
                help_text = (
                    "[SERVER] Available commands:\n"
                    "  server:who   - Show online users\n"
                    "  server:exit  - Disconnect from chat\n"
                    "  server:help  - Show this help message\n"
                    "  <user>:<msg> - Send a private message to a user\n"
                )
                client_socket.send(help_text.encode('utf-8'))
            else:
                recipient, dm_message = parse_message(message)
                if recipient and dm_message:
                    sent = False
                    for c, user in clients.items():
                        if user == recipient:
                            c.send(f"[DM from {username}] {dm_message}".encode('utf-8'))
                            sent = True
                            break
                    if not sent:
                        client_socket.send(f"[SERVER] Recipient '{recipient}' not found.".encode('utf-8'))
                else:
                    broadcast(f"{username}: {message}", client_socket)

    except Exception as e:
        logging.error("[SERVER] Exception in client handler for %s: %s", clients.get(client_socket, "unknown"), e)
    finally:
        user_left = clients.get(client_socket, "Unknown")
        remove_client(client_socket)
        broadcast(f"[SERVER] {user_left} has left the chat.")

def start_server():
    """Starts the server and listens for incoming client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info("[SERVER] Chat server started on %s:%d", HOST, PORT)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            logging.info("[SERVER] New connection from %s:%d", *addr)
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    except KeyboardInterrupt:
        logging.info("[SERVER] Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
