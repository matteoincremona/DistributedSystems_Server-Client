import socket
import threading
from file_pb2 import messaggio

size = 1024
enc_s = 'utf-8'
server_id = 0
ip = '127.0.0.1'
port = 8080
address = (ip, port)

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address))
    print("Client started")
    message = messaggio()
    message.to = server_id

    try:
        u_input = ''
        while u_input != 'end':
            u_input = input("Type your message: ")
            message.msg = u_input
            message_bytes = message.SerializeToString()
            client_socket.sendall(message_bytes)
            server_response = client_socket.recv(size).decode(enc_s)
            print("[Server response]:\n" + server_response)

    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":    
    main()