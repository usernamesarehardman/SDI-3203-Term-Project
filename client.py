import socket
import threading
import logging

HOST = "127.0.0.1"
PORT = 5555

def receive_messages(client_socket):
    """Continuously listens for and prints messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("[ERROR] Disconnected from server.")
            client_socket.close()
            break

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def receive_messages(client_socket):
    """Continuously listens for and logs messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            logging.info("[RECEIVED] %s", message)
        except Exception as e:
            logging.error("[ERROR] Disconnected from server: %s", e)
            client_socket.close()
            break

def start_client():
    """Starts the client connection and handles sending messages to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("[CLIENT] Connecting to server %s:%d", HOST, PORT)
    client_socket.connect((HOST, PORT))

    username = input("Enter your username: ")
    logging.info("[CLIENT] Username entered: %s", username)
    client_socket.send(username.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    if "Username already taken" in response:
        logging.warning("[CLIENT] %s", response)
        client_socket.close()
        return

    logging.info("[CLIENT] %s", response)
    logging.info("[CLIENT] Type 'server:exit' to leave, 'server:who' to list users.")
    logging.info("[CLIENT] To send a message, use '<recipient>:<message>' (e.g., bob:Hello!)")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == "server:exit":
            logging.info("[CLIENT] Exiting chat.")
            break
        logging.debug("[CLIENT] Sending message: %s", message)
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    logging.info("[CLIENT] Connection closed.")

if __name__ == "__main__":
    start_client()
