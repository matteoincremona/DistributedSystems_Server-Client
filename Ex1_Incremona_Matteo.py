import socket

# SERVER

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'

def main():

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)
        server.listen()
        print(f'Server is listening and waiting for a client on {ip}:{port}')

        # Accepting connection:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Receiving and printing a text message:
        c_msg = client_socket.recv(size).decode(enc_s)
        print(f"New message received: {c_msg}")

        # Replying to let the client know the message has arrived:
        rep = "Server has received your message"
        rep = rep.encode(enc_s)
        client_socket.send(rep)

    # In case of exeptions:
    except Exception as fail:
        print(f'There was an error: {fail}')

    # Closing the connection:
    finally:
        client_socket.close()
        print("Connection closed")
        server.close()


if __name__ == '__main__':
    main()
