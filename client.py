import time
import socket
from flask import Flask, render_template, request, redirect , url_for

def con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9997)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

def vid(id):
    message = bytes(id, 'utf-8')
    sock.send(message)
    exists = recieve()
    return exists

def recieve():
    while True:
        data = sock.recv(1024)
        return str(data, 'utf-8')

def vote(id):
    message = bytes(id, 'utf-8')
    sock.send(message)
    exists = recieve()
    return exists

def close():
    sock.send(bytes("exit",'utf-8'))    
    sock.close()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def voter():
    try:
        close()
    except:
        pass
    con()
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        response = vid(voter_id)
        if response == "true":
            return redirect('/vote')
        elif response == "done":
            return "Already Voted!"
        else:
            return "Not eligible to vote!"
    else:
        return render_template("voter.html")

@app.route('/vote', methods=['POST', 'GET'])
def candidate():
    if request.method == 'POST':
        candidate_id = request.form['candidate_id']
        response = vote(candidate_id)
        if response == "false":
            return "Candidate does not exist!"
        else:
            close()
            return render_template("thank.html")
    else:
        return render_template("candidate.html")

if __name__ == "__main__":
    app.run(debug=True)
