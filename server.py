import socket
import threading

clients = []

def send_message(message, sender_socket):
    for client in clients:
        try:
            client.sendall(message)
        except:
            client.close()
            clients.remove(client)

def accept_client(client_socket, addr):
    clients.append(client_socket)
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            send_message(msg, client_socket)
        except:
            break

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen()

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=accept_client, args=(client_socket, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    main()
