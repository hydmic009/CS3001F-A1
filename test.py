from socket import *
import threading

SERVER_IP = '172.31.48.1'
SERVER_PORT = 9596

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((host, port))
client_socket = socket(AF_INET, SOCK_STREAM)

# I NEED A THREAD FOR ACCEPTING AND RECEIVING MESSAGES


def login(sock, name, username, secret):
    request = f"LGN {name} {username} {secret}"
    sock.send(request.encode())
    receive()
   # response = sock.recv(1024).decode()
   # print(response)

def send_message(sock, peer_username, SERVER_IP, UDP_PORT):
    request = f"MSG {peer_username} {SERVER_IP} {UDP_PORT}"
    print("Message request sent to peer-waiting....")
    sock.send(request.encode())  #This sends a request to a server. 
   # client_socket.sendto(request.encode(), (SERVER_IP, UDP_PORT))
   # response, address = client_socket.recvfrom(1024)
   # print(response.decode())

def get_client_list(sock):
    request = "LST"
    sock.send(request.encode())
    receive()
  #  response = sock.recv(1024).decode()
   # print(response)

def disconnect(sock):
    request = "EXT"
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()

def receive():
    while True: 
       # message = client_socket.recv(1024).decode()
        message = client_socket.recv(1024).decode()
        if "LGN0" in message:
            print("Login Successful")

        if "LGN1" in message:
            print("Login failed")

        if "LST" in message:
            print("Current users in chat:")
            print(message[5:])
            print("\n")

        if "MSG0" in message:  #    if you get MSG0 you wait unitl you receive something else
           peer_info =  client_socket.recv(1024).decode().split(':') #This is waiting for a message
           peerIP = peer_info[2]  #This is the UDP port address
           peerPort = int(peer_info[3])
           print(peer_info)
        # else: 
        #      peer_info = message.split(':')
        #      peerIP = peer_info[2]
        #      peerPort = int(peer_info[3])

        #      UDPSend(peerIP, peerPort)
        
      #  peerIP = peer_info[2]
       # peerPort = int(peer_info[3])
            
        listener = threading.Thread(target=listenToPeer, daemon=True, args=(client_socket,))
        listener.start()

          #create listener threads here: once you've requested to message someone. After someone send a message back-create it This is so that you can receive messages while writing them. 
        

        if "MSG1" in message:  #What you receive is their info. with UDP socket info. 
             peer_info = message.split(':')
             peerIP = peer_info[2]
             peerPort = int(peer_info[3]) 
             listenToPeer()
             UDPSend(peerIP,peerPort)

            

      
        #Make a listener thread after MSG0 to listen to input in the background- it's a daemon thread. 

        


    #     while True: 

    #     UDPClient.bind(ip, UDP_port)
    #     UDPClient.recvfrom(1024),,,
    #     UDPClient.sendto(message.encode(), (ip, port))
        
        
def UDPSend(peerIP,peerPort):
         udp_socket = socket(AF_INET, SOCK_DGRAM)
         #udp_socket.bind((SERVER_IP, peerPort))
         udp_socket.bind(('0.0.0.0', 0))

         while True:
             message = input('>')
             if message.lower() == 'exit':
                 break
             udp_socket.sendto(message.encode(), (peerIP, peerPort))

         udp_socket.close()

        #  while True:
        #     message = input('>')
        #     udp_socket.bind(peerIP, peerPort)
        #     udp_socket.recvfrom(1024)
        #     udp_socket.sendto(message.encode(), (SERVER_IP,UDP_PORT))
          #   message = UDPclient.recvfrom(2014)
           #  print(message)
         #    pass
        
def listenToPeer(sock, peerPort):
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.bind((SERVER_IP, peerPort))

        while True:
             data, addr = sock.recvfrom(1024)
             print(data.decode())
            
      
        # while True:
        #     data = sock.recv(1024)
        #     print(data)
    
       #listenToPeer ( sock, name) : To receive and type atst
    #While true:
    #data = recvfrom(1024)
    #print(data)
            

def main():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    name = input("Enter your name: ")
    username = input("Enter your username: ")
    secret = input("Enter your secret: ")

    login(client_socket, name, username, secret)

    while True:
        print("\nOptions:")
        print("1. Send Message")
        print("2. Get Client List")
        print("3. Disconnect")
        
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            peer_username = input("Enter peer username: ")
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #Randomly generate a port #
            UDP_PORT = 9999
            udp_socket.bind((SERVER_IP,UDP_PORT))
            #we have to send the new UDP IP to the server and gives it to the peer. It sends back to you MSG0 to say that the message has been sent. When you get that wait until you hear back from client. 
            print(f"UDP socket created on {SERVER_IP}. Address sent to server ")
            send_message(client_socket, peer_username, SERVER_IP, UDP_PORT)
        elif choice == '2':
            get_client_list(client_socket)
        elif choice == '3':
            disconnect(client_socket)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

    #MSG1 means that the person has already messaged and so the connection has been made. You have both agreed to message each other 
    #We just use a while loop to receive messages in a separate thread

    #listenToPeer ( sock, name) : To receive and type atst
    #While true:
    #data = recvfrom(1024)
    #print(data)