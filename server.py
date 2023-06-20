import socket
import time

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4001))
s.listen(5)

def addHeader(str):
    return f'{len(str):<{HEADERSIZE}}'+str
while True:
    clientSocket, address = s.accept()
    print(f"Connection from {address} established.")

    msg = 'Welcome to the server!'
    msg = addHeader(msg)
    clientSocket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        timeMsg = f'The time is {time.time()}'
        headedTimeMsg = addHeader(timeMsg) 
        clientSocket.send(bytes(headedTimeMsg, 'utf-8'))
