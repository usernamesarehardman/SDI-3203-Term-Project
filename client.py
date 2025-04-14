import socket
import threading
import logging

# Configuration
HOST = "127.0.0.1"
PORT = 5555
MAX_MESSAGE_SIZE = 1024

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def receive_messages(client_socket):
    """Continuously listens for and logs messages from the server."""
    while True:
        try:
            message = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8')
            if not message:
                logging.warning("[CLIENT] Server closed the connection.")
                break
            logging.info("[RECEIVED] %s", message)
        except Exception as e:
            logging.error("[CLIENT] Disconnected from server: %s", e)
            break
    client_socket.close()

def start_client():
    """Starts the client connection and handles sending messages to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        logging.info("[CLIENT] Connecting to server %s:%d", HOST, PORT)
        client_socket.connect((HOST, PORT))
    except Exception as e:
        logging.error("[CLIENT] Could not connect to server: %s", e)
        return

    username = input("Enter your username: ").strip()
    while not username:
        username = input("Username cannot be empty. Enter a valid username: ").strip()
    logging.info("[CLIENT] Username entered: %s", username)
    registration_message = f"server:register {username}"
    client_socket.send(registration_message.encode('utf-8'))

    response = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8')
    if "Username already taken" in response or "Invalid registration format" in response:
        logging.warning("[CLIENT] %s", response)
        client_socket.close()
        return

    logging.info("[CLIENT] %s", response)
    logging.info("[CLIENT] Type 'server:exit' to leave, 'server:who' to list users.")
    logging.info("[CLIENT] Type 'server:help' to show all available commands.")
    logging.info("[CLIENT] To send a message, use '<recipient>:<message>' (e.g., bob:Hello!)")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == "server:exit":
            logging.info("[CLIENT] Exiting chat.")
            break
        if len(message.encode('utf-8')) > MAX_MESSAGE_SIZE:
            logging.warning("[CLIENT] Message too long. Keep it under %d bytes.", MAX_MESSAGE_SIZE)
            continue
        logging.debug("[CLIENT] Sending message: %s", message)
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            logging.error("[CLIENT] Failed to send message: %s", e)
            break

    client_socket.close()
    logging.info("[CLIENT] Connection closed.")

if __name__ == "__main__":
    start_client()
