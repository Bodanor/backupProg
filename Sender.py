import curses
import socket
import time
import os

#CHANGER CECI :
IP = "94.106.242.73"
PORT = 4444
ROOT = "."

HEADERSIZE = 100

#parametrage de curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.start_color()
curses.use_default_colors()

curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)


start_backup = time.time()
try:
    server_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_backup.connect((IP, PORT))

    total_size_send = 0
    total_size_local = 0

    total_file_send = 0
    total_file_local = 0


    files_list = []

    for path, subdirs, files in os.walk(ROOT):
        for name in files:
            file = os.path.join(path, name)
            files_list.append(file)

    for file_name in files_list:
        file_size = os.path.getsize(file_name)
        total_size_local += file_size
        total_file_local += 1

    for file_name in files_list:

        status_label = f"Connecté à {IP}"
        max_y, max_x = stdscr.getmaxyx()
        x = max_x //2 - len(status_label) // 2
        stdscr.move(0,x)
        stdscr.clrtoeol()
        stdscr.addstr(0, x, status_label)
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

            server_backup.sendall(data)
            for i in range(5,14):
                stdscr.move(i,0)
                stdscr.clrtoeol()

            stdscr.addstr(5,0,f"En attente de confirmation pour : \"{file_name.decode()}\"")
            stdscr.refresh()
            status_header = server_backup.recv(HEADERSIZE)
            if not status_header:
                stdscr.clear()
                ending_text = f"[ERREUR] le fichier {file_name.decode()} n'as pas pu être envoyé !"
                max_y, max_x = stdscr.getmaxyx()
                x = max_x // 2 - len(ending_text) // 2
                y = max_y // 2
                stdscr.addstr(y, x, ending_text)
                server_backup.close()
                c = stdscr.getch()
                exit(0)

            status_length = int(status_header.decode().strip())
            status = server_backup.recv(status_length)
            if status.decode() == "OK":
                total_size_send += int(file_size)

                for i in range(14,max_y):

                    stdscr.move(i,0)
                    stdscr.clrtoeol()
                stdscr.addstr(14,0,f"Fichier : \"{file_name.decode()}\" envoyé en [{round(time.time() - start_time, 2)}] secondes !")
                stdscr.refresh()
                string_mb = f"{round(total_size_send / 1024 ** 2, 2)} MB sur {round(total_size_local / 1024 ** 2, 2)} MB"
                max_y, max_x = stdscr.getmaxyx()
                stdscr.move(1, 0)
                stdscr.clrtoeol()
                stdscr.addstr(1,max_x - len(string_mb),string_mb)
                stdscr.refresh()
                string_nb_file = f"{total_file_send}/{total_file_local} envoyés"
                max_y, max_x = stdscr.getmaxyx()
                stdscr.move(max_y-1, 0)
                stdscr.clrtoeol()
                stdscr.addstr(max_y-1, max_x - len(string_nb_file)-1, string_nb_file)
                stdscr.refresh()

                total_file_send+= 1

            else:
                stdscr.clear()
                ending_text = f"[ERREUR] Le fihier {file_name.decode()} n'as pas pu être sauvegarder sur le serveur distant !"
                max_y, max_x = stdscr.getmaxyx()
                x = max_x // 2 - len(ending_text) // 2
                y = max_y // 2
                stdscr.addstr(y, x, ending_text)
                server_backup.close()
                c = stdscr.getch()
                exit(0)


    server_backup.close()
    stdscr.clear()
    ending_text = f"[INFO] Backup crée sur le serveur ! Temps d'envois total : {round(time.time() - start_backup, 2)} secondes"
    max_y, max_x = stdscr.getmaxyx()
    x = max_x // 2 - len(ending_text) // 2
    y = max_y // 2
    easter_text = "TRISMOQUE21 POWER !!!"
    stdscr.addstr(max_y - 1, max_x - len(easter_text) - 1, easter_text)
    stdscr.addstr(max_y - 1, max_x - len(easter_text) - 1, easter_text)
    stdscr.addstr(y, x, ending_text)
    stdscr.refresh()
    c = stdscr.getch()

except KeyboardInterrupt:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

except ConnectionRefusedError:
    stdscr.clear()
    ending_text = f"[ERREUR] Impossible de se connecter au serveur !"
    max_y, max_x = stdscr.getmaxyx()
    x = max_x // 2 - len(ending_text) // 2
    y = max_y // 2
    stdscr.addstr(y, x, ending_text)
    c = stdscr.getch()



#Arret de curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

