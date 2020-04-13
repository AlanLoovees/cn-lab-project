import socket

def con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

def vid():
    id = input("Enter the voter id: ")
    message = bytes(id, 'utf-8')
    sock.send(message)
    exists = recieve()
    return exists

def recieve():
    while True:
        data = sock.recv(1024)
        return str(data, 'utf-8')

def vote():
    id = input("Candidate that you vote for: ")
    message = bytes(id, 'utf-8')
    sock.send(message)
    exists = recieve()
    if(exists == "false"):
        print("Candidate does not exist!")
    else:
        print('Thank you for voting!')

def close():
    sock.send(bytes("exit",'utf-8'))    
    sock.close()

con()
response = vid()
if response == "true":
    vote()
else:
    print("Not eligible to vote!")
close()