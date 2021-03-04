import socket
import threading
import os

IP = "127.0.0.1"
PORT = 4444

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((IP, PORT))
sock.listen(0)
print("Server receiver Started !")


def client_handler(conn):
    if not os.path.exists("Backup"):
        os.mkdir("Backup")

    while True:
        file_name = conn.recv(100)
        if not (file_name):
            print("No more files !")
            break
        file_name = file_name.decode()

        file_size = conn.recv(100).decode()

        file_name = "Backup/" + file_name
        if not os.path.exists(os.path.dirname(file_name)):
            os.mkdir(os.path.dirname(file_name))

        with open(file_name, "wb") as file:
            c = 0

            while c < int(file_size):
                data = conn.recv(1024)
                if not (data):
                    break
                file.write(data)
                print(c)
                print(data)
                c += len(data)

            print("One file !")



while True:
    conn , addr = sock.accept()
    print(f"New connection from {addr[0]} on port {addr[1]}")
    client_thread = threading.Thread(target=client_handler, args=(conn,))
    client_thread.start()



