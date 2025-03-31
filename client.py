import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

# Receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("[ERROR] Disconnected from server.")
            client_socket.close()
            break

# Start client connection
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    if "Username already taken" in response:
        print(response)
        client_socket.close()
        return

    print("[CONNECTED] Type 'server:exit' to leave, 'server:who' to list users.")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == "server:exit":
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    start_client()
