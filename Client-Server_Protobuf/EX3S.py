import socket
import threading
from ex3file_pb2 import messaggio, handshake

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'
server_id = 0   # I chose a random value
err = False

def cl(client_socket, client_id):
    prefix = f"Client[{client_id}]: "

    try:
        mx = ""
        while mx != 'end':
            mx = client_socket.recv(size).decode(enc_s)
            messaggio.msg = mx
            messaggio.fro = client_id
            messaggio.to = server_id
            if not mx:
                break

            print(f"New message <{messaggio.msg}> from client [{messaggio.fro}] to server[{messaggio.to}]")

            response = f"Message <{messaggio.msg}> from client[{messaggio.fro}] successfully received"
            client_socket.sendall(response.encode(enc_s))

    except Exception as e:
        print(e)

    finally:
        print(f"Closing connection with {prefix}")
        client_socket.close()

# Operator function
def operator():
    while True:
        command = input()
        if command == "num_users":
            num_users = threading.active_count() - 2
            print(f"Total number of connected users = {num_users}")
        else:
            print("Command not found")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen()
    print(f'Server is listening and waiting for a client on {ip}: {port}...')

    client_id = 0
    operator_thread = threading.Thread(target = operator)
    operator_thread.daemon = True
    operator_thread.start()
    err = False

    while err == False:

        try:
            client_socket, client_address = server.accept()
            client_id += 1
            client_thread = threading.Thread(target = cl, args=(client_socket, client_id))
            client_thread.start()
            handshake.id = client_id
            handshake.error = err
            print(f"New client[{handshake.id}] and error: [{handshake.error}]")
            hndsh_message = f"[Handshake Message] Accepted connection from server[{server_id}] to client[{handshake.id}]\nError: [{handshake.error}]"
            client_socket.sendall(hndsh_message.encode(enc_s))

        except Exception as e:
            err = True
            handshake.error = err
            print(f'Error: [{handshake.error}]\nFailed connection with the client[{handshake.id}\nExeption raised: {e}]')

if __name__ == '__main__':
    main()