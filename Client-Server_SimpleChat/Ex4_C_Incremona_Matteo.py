import socket

# CLIENT

ip = '127.0.0.1'
port = 8080
address = (ip, port)
size = 1024
enc_s = 'utf-8'

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    print(f'Client connected to server at {ip}:{port}')

    while True:
        msg = input('Type your message: ').encode(enc_s)
        client.send(msg)

        # Receiving a message from the server:
        rep = client.recv(size)
        rep = rep.decode(enc_s)
    
        if rep.lower() == "fine":
            break
    
        print(f'New message: {rep}')

    client.close()
    print("Connection to server closed")


if __name__ == '__main__':
    main()

