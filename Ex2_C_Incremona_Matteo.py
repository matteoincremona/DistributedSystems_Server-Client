import socket

# CLIENT

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'

def main():

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        print(f'Client connected to server at {ip}: {port}')

        msg = input('Type your message: ').encode(enc_s)
        client.send(msg)

        # Receiving a message from the server:
        rep = client.recv(size)
        rep = rep.decode(enc_s)
        print(f'New message received: {rep}')

    except Exception as fail:
        print(f'There was an error: {fail}')

    finally:
        print("Connection closed")
        client.close()


if __name__ == '__main__':
    main()
    






    

        