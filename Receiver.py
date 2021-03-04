import socket
import threading
import os
import time
import datetime

IP = "127.0.0.1"
PORT = 4444

HEADERSIZE = 100

dest_folder = "Backup"

start_server_timer = time.time()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((IP, PORT))
sock.listen(0)
print(f"[{time.time() - start_server_timer}]Server receiver Started !")


def client_handler(conn):
    global dest_folder

    folder_info = datetime.datetime.now()
    dt_string = folder_info.strftime("_%d%m%y_%H:%M:%S")
    dest_folder_local = dest_folder + dt_string + "/"

    if not os.path.exists(dest_folder_local):
        os.mkdir(dest_folder_local)
    starting_connection_timer = time.time()

    while True:

        file_name_header = conn.recv(HEADERSIZE)
        if not (file_name_header):
            print("All files received !")
            print(f"Collected all files in {time.time() - starting_connection_timer} seconds")
            break

        file_name_length = int(file_name_header.decode().strip())
        file_name = conn.recv(file_name_length).decode()
        file_size_header = conn.recv(HEADERSIZE)

        if not (file_size_header):
            print("Something went wrong !")
            break
        file_size_length = int(file_size_header.decode().strip())
        file_size = int(conn.recv(file_size_length).decode())


        file_name = dest_folder_local + file_name
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        file_transfer_timer = time.time()
        with open(file_name, "wb") as file:
            count = 0

            while count < file_size:
                data = conn.recv(8192)
                if not data:
                    break
                file.write(data)

                count += len(data)

        print("OK")
        status = "OK".encode()
        status_header = f"{len(status) : < {HEADERSIZE}}".encode()
        conn.sendall(status_header + status)
        print(f"File \"{file_name}\" received in {time.time() - file_transfer_timer}")


while True:
    conn , addr = sock.accept()
    print(f"[{time.time() - start_server_timer}]New connection from {addr[0]} on port {addr[1]}")
    client_thread = threading.Thread(target=client_handler, args=(conn,))
    client_thread.start()
