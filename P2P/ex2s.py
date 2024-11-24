import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

clients_dict = {} # Same as ex 1
buffer = {} # In order to store the message for the clients not connected, I create a buffer as a dictionary.

def send_message(conn, m):
    serialized = m.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder='big'))
    conn.sendall(serialized)

def receive_message(conn, m):
    msg = m()
    size = int.from_bytes(conn.recv(4), byteorder='big')
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg

def handle_client(conn: socket.socket, addr):
    try:
        handshake = receive_message(conn, FastHandshake)
        requested_id = handshake.id
        
        if requested_id in clients_dict:
            id = max(clients_dict.keys()) + 1
            error = True
        else:
            id = requested_id
            error = False

        handshake = FastHandshake(id=id, error=error)
        send_message(conn, handshake)

        print(f'New client [{id}]\n')
        clients_dict[id] = conn

        if id in buffer:
            for buffered_message in buffer[id]:
                send_message(conn, buffered_message)
            buffer.pop(id, None)  

        while True:
            try:
                msg = receive_message(conn, Message)
                print(f'New message:\n>> {msg.msg}\n- Sender: {msg.fr}\n- Receiver: {msg.to}\n')

                if msg.to in clients_dict:
                    send_message(clients_dict[msg.to], msg)
                else:
                    if msg.to not in buffer:
                        buffer[msg.to] = []
                    buffer[msg.to].append(msg)
                    print(f'!!! Client {msg.to} not connected.\n')
                    print(f'-> Buffered message for client {msg.to}')

                if msg.msg == 'end':
                    break
            except:
                break
        
        print(f'Closing connection to [{id}].\n')
    finally:
        clients_dict.pop(id, None)
        conn.close()

def repeat_main(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            print(f'Server is listening and waiting for a client on {port}...')
            s.listen()
            while True:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        print(f'Error: {e}')

def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    repeat_main(port)

if __name__ == '__main__':
    main()
