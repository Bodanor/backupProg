import os
import socket
import time


IP = "127.0.0.1"
PORT = 4444
ROOT = "/"


HEADERSIZE = 100

start_backup = time.time()
server_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_backup.connect((IP, PORT))

print(f"Connecté à {IP}")


files_list = []

for path, subdirs, files in os.walk(ROOT):
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

        print(f"En attente de confirmation pour ! {file_name}")
        status_header = server_backup.recv(HEADERSIZE)
        if not status_header:
            print("[ERREUR] Envoie échoué !")
            exit(0)

        status_length = int(status_header.decode().strip())
        status = server_backup.recv(status_length)
        print(status)
        print(f"Fichier {file_name} envoyé en {round(time.time() - start_time, 2)} secondes !")

print(f"[INFO] Backup crée sur le serveur ! Temps d'envois total {round(time.time() - start_backup, 2)}")