import socket

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4001))

while True:
    fullMsg = ''
    newMsg = True
    while True:
        msg = s.recv(20)
        if newMsg:
            msgLen = int(msg[:HEADERSIZE])
            print(f"New message length: {msgLen}")
            newMsg = False
            
        fullMsg += msg.decode("utf-8")
        if len(fullMsg) - HEADERSIZE == msgLen:
            print("Full message recieved:", fullMsg[HEADERSIZE:])
            newMsg = True
            fullMsg = ''