# to be used with auth.py
import socket #, ssl
import threading
import os

import rsa

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def get_username():
    USER = os.getlogin()
    return USER

ip = get_ip()
IP = 'the-ip-where-auth.py-is-running'
port = 443
user = get_username()

public_key, private_key = rsa.newkeys(1024)
public_partner = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1("PEM"))

#else:
#    exit()

def sending_message(c, public_partner):
    while True:
        message = ip +  user
        c.send(rsa.encrypt(message.encode(), public_partner))
       
def receiving_message(c, private_key):
    while True:
        message = rsa.decrypt(c.recv(1024), private_key).decode()
        print(message)
        
threading.Thread(target=sending_message, args=(client, public_partner)).start()
threading.Thread(target=receiving_message, args=(client, private_key)).start()
