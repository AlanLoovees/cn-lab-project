import socket
from _thread import *
import threading

global flag
global true
global false
global done
global print_lock

print_lock = threading.Lock()

true = bytes("true", 'utf-8')
false = bytes("false", 'utf-8')
done = bytes("done", 'utf-8')

def con():
    global sock
    sock = socket.socket()
    server_address = ('localhost', 9997)
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(5)

def client_con():
    while True:
        c, addr = sock.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(recieve, (c,))

def recieve(connection):
    while True:
        data = connection.recv(1024)
        s = str(data, 'utf-8')
        with open('voters_list.txt','r') as voters:
            flag = -1
            for line in voters:
                for word in line.split():
                    if s == word:
                        flag = 0
                        with open('votes.txt','r') as votes:
                            for vote in votes:
                                for voted in vote.split():
                                    if s == voted:
                                        flag = 1
                                        connection.sendall(done)
        if flag == 0:
            connection.sendall(true)
        if flag == -1:
            connection.sendall(false)
            print_lock.release()
            break
        data = connection.recv(1024)
        cand = str(data, 'utf-8')
        with open('candidates_list.txt','r') as candidates:
            flag = 0
            for line in candidates:
                for word in line.split():
                    if cand == word:
                        flag = 1
                        connection.sendall(true)
                        f = open('votes.txt','a')
                        f.write(s+" "+cand+"\n")
                        f.close()
        if flag == 0:
            connection.sendall(false)
            print_lock.release()
            break
        data = connection.recv(1024)
        final = str(data, 'utf-8')
        if final == "exit":
            print("Vote Recorded!")
            print_lock.release()
            break

def close(s, data):
    print("Closing current connections")
    for i in range(2):
        connection[i].sendall(data)
        connection[i].close()
    print(s)

con()
client_con()
sock.close()
