# to be used with auth.py
import socket #, ssl
import threading
import os
import hashlib
import rsa

#import socket
#import threading


# List to store clients that are waiting for pairing
waiting_clients = []


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def get_username():
    #USER = os.getlogin()
    USER = 'iamserver'
    return USER

def hashing(ctext):
    obj = hashlib.sha256()
    obj.update(bytes(ctext, 'utf-8'))
    return obj.hexdigest()

#def sending_message(c):
#    while True:
#        message = ip +  user
#        c.send(rsa.encrypt(message.encode(), public_partner))
       
#def receiving_message(c):
#    while True:
#        message = rsa.decrypt(c.recv(1024), private_key).decode()
#        print(message)

#ip = get_ip()
ip = '0.0.0.0'
port = 443
user = get_username()

public_key, private_key = rsa.newkeys(1024)
public_partner = None



# Define a function to handle each client's communication
def handle_client(client_socket, client_address, public_partner, private_key):
    print(f"New connection from {client_address}")
    # Try pairing with an existing client from the waiting_clients list
    if waiting_clients:
        paired_client = waiting_clients.pop(0)
        paired_socket, paired_address = paired_client
        # Notify both clients that they are paired
        #client_socket.send(f"You're paired with {paired_address}".encode())
        #client_socket.send(rsa.encrypt(f"You're paired with {paired_address}".encode(), public_partner))

        #paired_socket.send(f"You're paired with {client_address}".encode())
        #paired_socket.send(rsa.encrypt("You're paired with {client_address}".encode(), public_partner))
        
        # Now, we can start communication between the two
        while True:
            print('in waiting-clients')
            try:
                # Receive and forward data between paired clients
                #msg = client_socket.recv(1024)
                message_A = rsa.decrypt(client_socket.recv(1024), private_key).decode()
                print(message_A)
                message_B = rsa.decrypt(paired_socket.recv(1024), private_key).decode()
                print(message_B)
                if message_A:
                    #paired_socket.send(msg)
                    message_B = hashing(message_B)
                    print(message_B)
                    paired_socket.send(rsa.encrypt(message_B.encode(), public_partner))
                    paired_socket.send(rsa.encrypt(b'%s' % "CTRU".encode(), public_partner))
                else:
                    break
                if message_B:
                    message_A = hashing(message_A)
                    print(message_A)
                    client_socket.send(rsa.encrypt(message_A.encode(), public_partner))
                    client_socket.send(rsa.encrypt(b'%s' % "CTRU".encode(), public_partner))
                else:
                    break
            except:
                break
        
        # Cleanup
        client_socket.close()
        paired_socket.close()
    
    else:
        # If no pairing is available, add to the waiting list
        waiting_clients.append((client_socket, client_address))
        #client_socket.send("You're in the waiting list. Please wait for a pair.".encode())
        #client_socket.send(rsa.encrypt("You're in the waiting list. Please wait for a pair".encode(), public_partner))


# Server setup
def start_server():
#    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    server.bind(('0.0.0.0', 12345))
#    server.listen(5)
#    print("Server started. Waiting for connections...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print("Server started. Waiting for connections...")

    while True:
#        client_socket, client_address = server.accept()
        client_socket, client_address = server.accept()
        client_socket.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))


        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, public_partner, private_key))
        client_thread.start()

if __name__ == "__main__":
    start_server()





#choice = input("Do you want to host (1) or to connect (2): ")

#if choice == "1":

#elif choice == "2":
#    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    client.connect(("192.168.101.112", port))
#    public_partner = rsa.PublicKey.loadpkcs1(client.recv(1024))
#    client.send(public_key.save_pkcs1("PEM"))
#
#else:
#    exit()

#threading.Thread(target=sending_message, args=(client,)).start()
#threading.Thread(target=receiving_message, args=(client,)).start()



