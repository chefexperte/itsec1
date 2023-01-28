import socket
import time

HOST = "it-sec-challenge.urz.uni-heidelberg.de"
PORT = 10002

MAIL = "jb007@stud.uni-heidelberg.de"

# geklaut von Wikipedia: https://en.wikipedia.org/wiki/MD4#MD4_collision_example
k1="839c7a4d7a92cb5678a5d5b9eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edd45e51fe39708bf9427e9c3e8b9"
k2="839c7a4d7a92cbd678a5d529eea5a7573c8a74deb366c3dc20a083b69f5d2a3bb3719dc69891e9f95e809fd7e8b23ba6318edc45e51fe39708bf9427e9c3e8b9"

# convert hex to bytes to prevent encoding problems
b1=bytes.fromhex(k1)
b2=bytes.fromhex(k2)

### ---- HELPER FUNCTIONS ---- ###

def sRead(s: socket.socket):
    print("[Server]")
    msg = s.recv(4096).decode()
    print(msg)
    time.sleep(0.1)
    print("")
    return msg

def sWrite(s: socket.socket, msg: str):
    print("[Client]")
    print(msg)
    s.send((msg+"\n").encode())
    print("")
    time.sleep(0.1)

def sWriteB(s: socket.socket, msg: str):
    print("[Client]")
    print(msg.hex())
    s.send((msg + b"\n"))
    print("")
    time.sleep(0.1)


### ---- ACTUAL CODE ---- ###

# connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# get initial prompt and wait for mail-request
sRead(s)
sRead(s)

# send mail-address
sWrite(s,MAIL)

# create file with hash-collision
sRead(s)
sWrite(s, "3")
sRead(s)
sWriteB(s, b1)
sRead(s)
sWrite(s, "Oops I did it again!")

# rename top_secret
sRead(s)
sWrite(s, "2")
sRead(s)
sWrite(s, "top_secret")
sRead(s)
sWriteB(s, b2)

#try to read
sRead(s)
sWrite(s, "4")
sRead(s)
sWriteB(s, b1)
msg = sRead(s)
sWrite(s, "7")
sRead(s)

print("Die Flag ist:")
print(msg.split("\n")[2])
