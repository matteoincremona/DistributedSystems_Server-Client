import socket
import threading

# SERVER

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'
count = 0

def main():
        global count
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)
        server.listen()
        print(f'Server is listening and waiting for a client on {ip}: {port}')

        # Accepting multiple connection:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        count = count + 1
        print(f'Tot. number of clients = {count}')

        thread = threading.Thread(target = f_client, args = (client_socket, client_address,))
        thread.start()

        while count >= 1:
            # Accepting multiple connection:
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            count = count + 1
            print(f'Tot. number of clients = {count}')

            thread = threading.Thread(target = f_client, args = (client_socket, client_address,))
            thread.start()

            if count == 0:
                print("All connection closed")
                client_socket.close()
                server.close()
                break


def f_client(client_socket, client_address):

    global count
    try:

        while True:
            m = client_socket.recv(size)
            m = m.decode(enc_s)

            # 'End' message:
            if m.lower() == 'end':
                client_socket.send("fine".encode(enc_s))
                break
            
            # Otherwise, the connection continues:
            print(f'New message received from client {client_address[1]}: {m}')
            reply = 'Server has received your message'
            client_socket.send(reply.encode(enc_s))

    except Exception as fail:
        print(f'There was an error: {fail}')
    finally:
        client_socket.close()
        print(f"Connection to client {client_address[1]} closed")
        count = count - 1
        print(f'Tot. number of clients = {count}')
        


if __name__ == '__main__':
    main()