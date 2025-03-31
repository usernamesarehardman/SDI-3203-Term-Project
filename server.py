import socket
import threading

# Server Configuration
HOST = "127.0.0.1"
PORT = 5555
clients = {}  # Dictionary to store client sockets and usernames

# Broadcast message to all clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  # Don't send message back to the sender
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Handle individual client
def handle_client(client_socket):
    try:
        # Receive username
        username = client_socket.recv(1024).decode('utf-8')
        if username in clients.values():
            client_socket.send("Username already taken. Try again.".encode('utf-8'))
            client_socket.close()
            return

        clients[client_socket] = username
        print(f"[NEW CONNECTION] {username} joined the chat.")
        broadcast(f"{username} has joined the chat!")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == "server:exit":
                break
            elif message.lower() == "server:who":
                user_list = ", ".join(clients.values())
                client_socket.send(f"Active Users: {user_list}".encode('utf-8'))
            else:
                broadcast(f"{username}: {message}", client_socket)

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        remove_client(client_socket)

# Remove client from the list
def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"[DISCONNECTED] {username} left the chat.")
        broadcast(f"{username} has left the chat.")
        del clients[client_socket]
        client_socket.close()

# Main function to start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[LISTENING] Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[CONNECTION] Connected by {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
