import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

clients_dict = {} # I want to store all the clients is a dictionary where the keys are the id and the values are the 
c_id = 0 # Each time a clients connects, its id will be +1 than the previous client.

def send(conn, m):
    serialized = m.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
    conn.sendall(serialized)

def receive(conn, m):
    msg = m()
    size = int.from_bytes(conn.recv(4), byteorder = 'big')
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg

def cl(connection: socket.socket, addr):
    global c_id
    id = c_id
    c_id += 1

    clients_dict[id] = connection
    with connection:
        handshake = FastHandshake(id=id, error=False)
        send(connection, handshake)
        print(f'New client [{id}]\n')

        while True:
            try:
                msg = receive(connection, Message)
                print(f'New message:\n>> {msg.msg}\n- Sender: {msg.fr}\n- Receiver: {msg.to}\n')
                
                if msg.to in clients_dict:
                    send(clients_dict[msg.to], msg)
                else:
                    print(f'!!! Client [{msg.to}] is not connected to the server.\n!!! Message dropped.\n')
                    
                if msg.msg == "end":
                    break

            except:
                break

        print(f'Closing connection to [{id}].\n')
        clients_dict.pop(id, None)

def repeat_main(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            print(f'Server is listening and waiting for a client on {port}...')
            s.listen()
            while True:
                try:
                    conn, addr = s.accept()
                    Thread(target = cl, args = (conn, addr)).start()
                except KeyboardInterrupt:
                    break
    except:
        pass

def main():
    port = 8080
    repeat_main(port)

if __name__ == '__main__':
    main()