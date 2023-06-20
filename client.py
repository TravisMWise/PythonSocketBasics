import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4002))

while True:
    fullMsg = b''
    newMsg = True
    while True:
        msg = s.recv(16)
        print(msg)
        if newMsg:
            msgLen = int(msg[:HEADERSIZE])
            print(f"New message length: {msgLen}")
            newMsg = False
            
        fullMsg += msg
        
        if len(fullMsg) - HEADERSIZE == msgLen:
            print("Full message recieved:", fullMsg[HEADERSIZE:])
            
            # When we have all the data for the stucture we are
            # done using the socket and can use the data as normal
            d = pickle.loads(fullMsg[HEADERSIZE:])
            print(d) # {1: 'Name', 2: 'Age'}
            print(d[1]) # Name
            print(d[2]) # Age

            newMsg = True
            fullMsg = b''