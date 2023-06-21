import socket
import time
import pickle


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4002))
s.listen(5)

while True:
    # Wait for a connection
    clientSocket, address = s.accept()
    print(f"Connection from {address} established.")

    # Get a data structure
    d = {1:'Name', 2:'Age'}
    
    # Package the data up for sending using pickle 
    msg = pickle.dumps(d)
    
    # Add a header with the length of the msg to send
    # Convert the header to bytes to match the msg and socket format
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg

    # Send the message
    clientSocket.send(msg)
