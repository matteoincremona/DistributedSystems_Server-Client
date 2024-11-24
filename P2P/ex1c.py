import socket
from sys import argv
from template_pb2 import Message, FastHandshake
import threading

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

def receive_messages(conn):
    while True:
        try:
            response = receive_message(conn, Message)
            print(f'\nNew message received:\n>> {response.msg}\n- From: {response.fr}\n- To {response.to}\nType your message: ')
        except:
            break

def main():
    host = '127.0.0.1'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print('Connected to the server')
        
        handshake = receive_message(s, FastHandshake)
        if handshake.error:
            print('Connection rejected.')
            return

        print(f'My ID: {handshake.id}')
        my_id = handshake.id

        thread = threading.Thread(target=receive_messages, args=(s,))
        thread.daemon = True  
        thread.start()

        while True:
            try:
                data = input('Type your message: ') 
                
                if ' ' not in data:
                    print('Message not valid. Example format: 1 ciao')
                    continue
                
                to_id, msg = data.split(' ', 1)
                to_id = int(to_id)

                if my_id == to_id:
                    print('!!! You sent a message to yourself.\n')

            except ValueError:
                print('Message not valid. Example format -> 1 ciao')
                continue

            except:
                msg = "end" # It doesn't matter the which id is provided if the message is 'end'. The client will be closed in all cases.
                target_id = id 

            message = Message(fr = my_id, to = to_id, msg = msg)
            send_message(s, message)

            if msg == "end":
                break
        
        print("Closing connection")

if __name__ == '__main__':
    main()
