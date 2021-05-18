import socket
import threading
import csv
# from dateutil import parser
from datetime import *
# from time import *
# from timeit import *

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def critical_section(conn, lock, msg, addr):
    count = 0
    lock.acquire()
    try:
        if msg == "req":
            print(f"CLIENT {addr} INTO CS")
            count += 1
            shared_res_req = "OK"
            conn.send(shared_res_req.encode(FORMAT))
            release = conn.recv(HEADER).decode(FORMAT)
            print(f"CLIENT {addr} OUT OF CS")
    finally:
        lock.release()

lock = threading.Lock()


def clients(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:

        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == "d":
            connected = False
            break
        x = len(msg) - 26
        critical_section(conn, lock, msg[:x], addr)

        # maintaining log file
        with open('log.csv', mode='a') as log:
            fieldnames = ['address', 'date', 'time', 'message']
            write = csv.DictWriter(log, fieldnames=fieldnames)
            address = str(addr[0]), str(addr[1])
            time_at_msg_recv = datetime.now()
            date = time_at_msg_recv.date()
            time = time_at_msg_recv.time()
            message = msg

            fill = {
                'address': address,
                'date': date,
                'time': time,
                'message': message
            }
            write.writerow(fill)

    print(f'Disconnected {addr}')


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    clients_conn = []
    while True:
        conn, addr = server.accept()
        active = threading.activeCount()

        thread = threading.Thread(target=clients, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] = {active}")


print("[STARTING] server is starting...")
start()
