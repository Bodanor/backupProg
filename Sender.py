import os
import socket
import time

IP = "127.0.0.1"
PORT = 4444

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
    server_backup.send(str(file_name).encode())
    time.sleep(0.1)
    server_backup.send(str(file_size).encode())
    time.sleep(0.1)
    with open(file_name, "rb") as file:
        c = 0

        start_time = time.time()
        while c <= file_size:
            data = file.read(1024)
            if not (data):
                break

            server_backup.sendall(data)
            c+=len(data)

        print(f"File {file_name} Sended in {time.time() - start_time} seconds ! ")
        time.sleep(0.1)
