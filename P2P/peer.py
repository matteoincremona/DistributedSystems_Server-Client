import socket
import struct
import threading
import time
from sys import argv
from template_pb2 import Message
from snowflake import derive_id

connected_peers = {}
processed_msgs = set()

# Send message
def transmit(conn, msg):
    try:
        serialized = msg.SerializeToString()
        conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
        conn.sendall(serialized)
    except Exception as e:
        print(f"!!! Exception: {e}")


# Receive message
def receive(conn, msg_type):
    try:
        size_data = conn.recv(4)
        if not size_data:
            return None
        size = int.from_bytes(size_data, byteorder="big")
        data = conn.recv(size)
        if not data:
            return None
        msg = msg_type()
        msg.ParseFromString(data)
        return msg
    except Exception as e:
        print(f"!!! Exception: {e}")
        return None


# Handle peer connections
def manage_peer(conn, addr):
    print(f"New peer connection from {addr}")
    try:
        while True:
            msg = receive(conn, Message)
            if msg is None:
                break

            msg_key = (msg.fr, msg.to, msg.msg)

            if msg_key not in processed_msgs:
                processed_msgs.add(msg_key)

                if msg.to == my_id:
                    print(f"New message received:\n>> '{msg.msg}'\n- Sender Peer: {msg.fr}")
                else:
                    print(f"Relaying message:\nFrom Peer {msg.fr}\nTo Peer {msg.to}")
                    relay_msg(msg, conn)
    except Exception as e:
        print(f"!!! Exception: {e}")
    finally:
        print(f"Closing connection to {addr}")
        conn.close()

def relay_msg(msg, source_conn):
    for peer_id, peer_conn in connected_peers.items():
        if peer_conn != source_conn:
            try:
                print(f"Relaying message '{msg.msg}' from Peer {msg.fr} to Peer {peer_id}")
                transmit(peer_conn, msg)
            except Exception as e:
                print(f"!!! Exception: {e}")

def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", port))
        server_socket.listen()
        print(f"Listening on port {port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Peer connected from {addr}")
            threading.Thread(target=manage_peer, args=(conn, addr), daemon=True).start()

def join_peer(peer_ip, peer_port):
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_ip, peer_port))
        peer_id = derive_id(int.from_bytes(peer_ip.encode(), byteorder="big"))
        connected_peers[peer_id] = peer_socket
        print(f"Connected to peer at {peer_ip}:{peer_port}")
        threading.Thread(target=manage_peer, args=(peer_socket, (peer_ip, peer_port)), daemon=True).start()
    except Exception as e:
        print(f"!!! Unable to connect to peer at {peer_ip}:{peer_port}: {e}")

def user_input():
    while True:
        try:
            data = input("Type: \n")
            if " " not in data:
                print("!!! Format not valid. Example -> ID ciao")
                continue
            
            target_id, msg = data.split(" ", 1)
            try:
                target_id = int(target_id)
            except ValueError:
                print("!!! Peer ID must be numeric.")
                continue

            message = Message(fr=my_id, to=target_id, msg=msg)

            for peer_id, peer_conn in connected_peers.items():
                print(f"Sending message <{msg}>\n- Receiver Peer: {target_id}\n- Middle Peer: {peer_id}")
                transmit(peer_conn, message)

            if msg.lower() == "end":
                print("Connection closed.")
                break
        except Exception as e:
            print(f"!!! Error: {e}")
            break

def create_id(preferred_id=None):
    if preferred_id is not None:
        return preferred_id

    packed_ip = socket.inet_aton("127.0.0.1")
    ip_as_int = struct.unpack("!I", packed_ip)[0]
    return derive_id(ip_as_int)

if __name__ == "__main__":
    try:
        my_ip_port = argv[1]
        my_ip, my_port = my_ip_port.split(":")
        my_port = int(my_port)

        preferred_id = None
        if "--desired-id" in argv:
            preferred_id_index = argv.index("--desired-id") + 1
            preferred_id = int(argv[preferred_id_index])

        peers_to_connect = []
        for i in range(2, len(argv)):
            if argv[i] != "--desired-id" and not argv[i].isdigit():
                peers_to_connect.append(argv[i])
    except (IndexError, ValueError):
        print('Run for example -> python peer.py 127.0.0.1:8083 --desired-id 77252666718255106\n')
        exit()

    my_id = create_id(preferred_id)
    # I changed the ID as the last 4 digits of the examples given in the file. (Just a way to change the IDs)
    # Of course, more peer connets, more is the probability to have same IDs (given that the lenght is the same for all peers).
    print(f"New: {str(my_id)[13:]}")

    threading.Thread(target=listen, args=(my_port,), daemon=True).start()

    for peer_conn in peers_to_connect:
        try:
            peer_ip, peer_port = peer_conn.split(":")
            threading.Thread(target=join_peer, args=(peer_ip, int(peer_port)), daemon=True).start()
        except ValueError:
            print(f"!!! Invalid peer connection format: {peer_conn}")

    user_input()

    while True:
        time.sleep(1)
