import socket
from datetime import *

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
ADDRESS = client.getsockname()[1]

while True:
    print("TO GET INTO CRITICAL SECTION TYPE - 'Y' or 'y'\n"
          "TO DISCONNECT PRESS 'd' or 'D'")
    while True:
        message = input("TYPE YOUR MESSAGE - ").lower()
        if message == "d" or message == "y":
            break
        print("PLEASE TYPE VALID MESSAGE")
    if message == 'd':
        client.send(str(message).encode(FORMAT))
        print("DISCONNECTING...")
        break
    if message == 'y':
        print("TO REQUEST SHARED RESOURCE 'A' TYPE - 'req' or 'REQ'")
        while True:
            req = input("TYPE YOUR MESSAGE - ").lower()
            if req == 'req':
                break
            print("PLEASE TYPE VALID MESSAGE")
        request = client.send(str(str(req) + str(datetime.now())).encode(FORMAT))
        req_ack = client.recv(HEADER).decode(FORMAT)
        print(f"ACKNOWLEDGEMENT FROM SERVER = {req_ack}")
        print("TO RELEASE SHARED RESOURCE 'A' TYPE - 'rel' or 'REL'")
        while True:
            rel = input("TYPE YOUR MESSAGE - ").lower()
            if rel == 'rel':
                break
            print("PLEASE TYPE VALID MESSAGE")
        rel_ack = client.send(str(rel).encode(FORMAT))
        print(f"RELEASING SHARED RESOURCE")
