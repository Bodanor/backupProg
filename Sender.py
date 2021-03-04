import os
import socket
import time


IP = "127.0.0.1"
PORT = 4444

HEADERSIZE = 100
server_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_backup.connect((IP, PORT))

print(f"Connected to {IP}")


root = "Envoi/"
files_list = []

for path, subdirs, files in os.walk(root):
    for name in files:
        file = os.path.join(path, name)
        files_list.append(file)

for file_name in files_list:

    file_size = os.path.getsize(file_name)
    file_size = str(file_size).encode()
    file_size_header = f"{len(file_size) : < {HEADERSIZE}}".encode()

    file_name = file_name.encode()
    file_name_header = f"{len(file_name) : < {HEADERSIZE}}".encode()

    server_backup.sendall(file_name_header + file_name)
    server_backup.sendall(file_size_header + file_size)

    with open(file_name, "rb") as file:
        start_time = time.time()
        data = file.read()
        print(server_backup.sendall(data))

        print("Waiting for status...")
        status_header = server_backup.recv(HEADERSIZE)
        if not status_header:
            print("FAILED !")

        status_length = int(status_header.decode().strip())
        status = server_backup.recv(status_length)
        print(status)
        print(f"File {file_name} Sended in {time.time() - start_time} seconds !")
        time.sleep(0.1)