import socket
import threading
import os
import time
import datetime

IP = "127.0.0.1"
PORT = 4444

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
        file_name = conn.recv(1000)
        if not (file_name):
            print("All files received ! !")
            print(f"Collected all files in {time.time() - starting_connection_timer} seconds")
            break
        file_name = file_name.decode()

        file_size = conn.recv(1000).decode()
        file_name = dest_folder_local + file_name
        print(file_name)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        file_transfer_timer = time.time()

        with open(file_name, "wb") as file:
            c = 0

            while c < int(file_size):
                data = conn.recv(1024)
                if not (data):
                    break
                file.write(data)
                c += len(data)

            print(f"File \"{file_name}\" received in {time.time() - file_transfer_timer}")


while True:
    conn , addr = sock.accept()
    print(f"[{time.time() - start_server_timer}]New connection from {addr[0]} on port {addr[1]}")
    client_thread = threading.Thread(target=client_handler, args=(conn,))
    client_thread.start()



