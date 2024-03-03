from socket import *
import threading
from ClientClass import *

HOST_IP = '172.31.48.1'
HOST_PORT = 9596
clients = {}
dict_lock = threading.Lock()

connectorSocket = socket(AF_INET, SOCK_STREAM)
connectorSocket.bind((HOST_IP, HOST_PORT))
connectorSocket.listen()
print(f"The server is running and listening for connections on {HOST_IP}:{HOST_PORT}")


def acceptClients():
    #Accept new connections sent to the connector socket and create a Thread to handle client
    while True:
        clientSocket, addr = connectorSocket.accept()
        print(f"Accepted connection from {addr}")
        clientThread = threading.Thread(target=handleClient, args=(clientSocket, addr))
        clientThread.start()

#TODO implement protocol that handles requests from clients
#? Should we use a 'keepAlive'?
def handleClient(sock, addr):

    client_username = 'noSignedIn'

    while True:
        #Turn message from client to server into str[] of args
        request = sock.recv(1024).decode().split(":")

        requestType = request[0]

        if requestType == 'LGN':
            print(f"Attempting login on {request[2]}")

            #Take in arguments
            name = request[1]
            username = request[2]
            secret = request[3]
            newClient = Client(name, username, secret, addr, sock)

            client_username = username

            #Print client name and requested peer
            print(f"CLIENT_NAME: {name}")
            print(f"CLIENT_USERNAME: {username}")
            print(f"CLIENT_SECRET: {secret}")

            if username not in clients.keys():
                with dict_lock:
                    clients[username] = newClient
                    print(f"New client {username} has logged in.")
                    #Send succesfull NEW login response to client
                    response = f"LGN0:{username}"
                    sock.send(response.encode())
            else:
                if clients[username].secret == secret:
                    print(f"{username} has logged in succesfully.")
                    #Send succesfull login response to client
                    #? SHOULD THIS BE A DIFFERENT CODE?
                    response = 'LGN0'
                    sock.send(response.encode())
                else:
                    #Send failed login response to client
                    print(f"Failed login attempt on {username} at {addr}.")
                    response = 'LGN1'
                    sock.send(response.encode())

        elif requestType == 'MSG':

            #Take in arguments
            peer_username = request[1]
            clientIP = request[2]
            clientPORT = request[3] #The port that you want the client to chat to you on. 

            #Print requested peer
            print(f"REQUESTED_PEER: {peer_username}")

            if peer_username in clients.keys():
                peerSock = clients[peer_username].socket
                #Send peer address and client address back to client
                clientAddr_str = f"MSG1:{client_username}:{clientIP}:{clientPORT}"  # sends to peer that I want to message 
                response = f"MSG0:{peer_username}"
                sock.send(response.encode())  #this sends message back to you
                peerSock.send(clientAddr_str.encode())  #This sends to peer

            else:
                print(f"There is no {peer_username} on the server.")
                response = 'MSG2'
                sock.send(response.encode())

        elif requestType == 'LST':
            clientList = ''
            for client in clients:
                clientList += str(client)+"\n"
            clientList = clientList[:-1] #remove last newline
            response = f"LST0:{clientList}"
            sock.send(response.encode())

        elif requestType == 'EXT':
            clients.pop(username)
            print(f"{peer_username} has disconnected from the server.")
            return

def main():
    acceptClients()

if __name__ == "__main__":
    main()