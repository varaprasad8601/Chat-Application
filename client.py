#client code
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            split_message = message.split("~")
            if len(split_message) >= 2:
                username = split_message[0]
                content = split_message[1]
                print(f"[{username}]{content}")
            else:
                print("Invalid message format received from the server")
        else:
            print("Message received from the server is empty")

def send_message_to_server(client, username):
    while 1:
        message_content = input("message: ")
        if message_content != '':
            message = f"{username}~{message_content}"
            client.sendall(message.encode())
        else:
            print("Empty message")
            exit(0)

def communicate_to_server(client, username):
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    threading.Thread(target=send_message_to_server, args=(client, username)).start()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to the server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")
    
    username = input("Enter username:")
    communicate_to_server(client, username)

if __name__ == "__main__":
    main()