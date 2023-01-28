import socket
import time
import re

HOST = "it-sec-challenge.urz.uni-heidelberg.de"
PORT = 10001

MAIL = "jb007@stud.uni-heidelberg.de"
PKEY = "1337"

### ---- HELPER FUNCTIONS ---- ###

def sRead(s: socket.socket):
    print("[Server]")
    msg = s.recv(4096).decode()
    print(msg)
    time.sleep(0.1)
    
    return msg

def sWrite(s: socket.socket, msg: str):
    print("[Client]")
    print(msg)
    s.send((msg+"\n").encode())
    print("")
    time.sleep(0.1)

### ---- ACTUAL CODE ---- ###

## GET ENCRYPTED FLAG

print("========   ERFRAGE DIE VERSCHLÜSSELTE FLAG   ========")

# connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# get initial prompt and wait for mail-request
sRead(s)
sRead(s)

# send mail-address
sWrite(s,MAIL)

# get variables
msg = sRead(s)
prime = (re.findall("prime =.*$",msg,re.MULTILINE)[0]).split(" ")[-1]
generator = (re.findall("generator =.*$",msg,re.MULTILINE)[0]).split(" ")[-1]
pub_key = msg.split("\n")[10]

# send X
X = pow(int(generator),int(PKEY)) % int(prime) 
sWrite(s, str(X))

# read prompt
msg = sRead(s)
enc_Flag= msg.split("\n")[2]

print("========  BERECHNE FLAG  ========")
print("Bekannte Variablen:")
print("prime:       " + prime)
print("generator:   " + generator)
print("pub_key_bob: " + pub_key)
print("priv_key:    " + PKEY)
print("enc_Flag:    " + enc_Flag)
print("")

secret_key = pow(int(pub_key),int(PKEY)) % int(prime)
b_secret_key = bin(secret_key)[2:].zfill(128)

print("Der geheime Schlüssel ist:")
print(secret_key)
print("In Binärdarstellung ist dies:")
print(b_secret_key)

print("")

b_enc_Flag = bin(int(enc_Flag))[2:].zfill(128)

equal_line = "="*128

print("XOR enc_Flag and secret_key")
print("enc_Flag:   " + b_enc_Flag)
print("secret_key: " + b_secret_key)
print("            " + equal_line)
b_dec_Flag = bin(int(b_enc_Flag,2)^int(b_secret_key,2))[2:].zfill(128)
print("dec_Flag:   " + b_dec_Flag)
print("")

print("Die Flag in lesbarer Form heißt:")

# convert to ASCII
dec_Flag = "".join([chr(int(b_dec_Flag[i:i+8],2)) for i in range(0,len(b_dec_Flag),8)])

# dangerous: reverse flag little -> big endian
print(dec_Flag[::-1])


