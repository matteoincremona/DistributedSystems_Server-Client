import socket
import threading

# To test, I used the template-client.py given (I didn't include it in the folder).

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'

def cl(client_socket, client_id):
    prefix = f"Client[{client_id}]: "

    try:
        mx = ""
        while mx != 'end':
            mx = client_socket.recv(size).decode(enc_s)
            if not mx:
                break

            print(prefix + mx)

            response = f"Server has received the message <{mx}> correctly.\n"
            client_socket.send(response.encode(enc_s))

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

    while True:
        client_socket, client_address = server.accept()
        print(f"New client from {client_address}")
        client_id += 1
        client_thread = threading.Thread(target = cl, args=(client_socket, client_id))
        client_thread.start()

if __name__ == '__main__':
    main()