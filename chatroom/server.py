import socket
import select

HEADER_LENGTH = 10
IP = '127.0.0.1' # Localhost
PORT = 4001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(5)

sockets_list = [server_socket]
clients = {} # Client's socket will be the key and user data will be the value

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if len(message_header) == 0:
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False
    
    
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        # If we get a new user i.e. a connection request to the server
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = recieve_message(client_socket)
            if not user:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print("Accepted new connection from {}:{} username:{}".format(
                client_address[0], 
                client_address[1], 
                user['data'].decode('utf-8')
            ))
        else:
            message = recieve_message(notified_socket)
            if not message:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user =  clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header']+user['data']+message['header']+message['data'])
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
