from socket import socket
from time import sleep
from threading import Thread
from colorama import Fore

_all_threads = []

def handle_client(conn, addr):
    print("[thread] Iniciando")
    print("[thread] client:", addr)
    while True:
        try:
            command = input(f"{Fore.LIGHTGREEN_EX}>>:{Fore.RESET} ")
            command = command.lower()
            if command == "exit" or command == "q":
                raise KeyboardInterrupt()
            else:
                conn.send(command.encode())
            # recv datos
            message = ""
            while True:
                chartter = conn.recv(1).decode()
                if chartter == ">": break
                elif chartter == "<": pass
                else: message += chartter
            message = conn.recv(int(message) + 10).decode()
            print("[thread] client:", addr, 'recv:', message)
        except (KeyboardInterrupt, EOFError):
            if input("Quiere finalizar el servidor? (s/n): ").lower() == "s":
                print("Servidor finalizado, use Ctrl + c para salir del programa")
                conn.close()
                exit(0)
    conn.close()
    print("[thread] ending")

def create_server():
    global _all_threads
    s = socket()
    s.bind(("0.0.0.0", 8888))
    s.listen(10)

    print("Servidor escuchando en 0.0.0.0:8888")
    conn, addr = s.accept()
    print(f"Conexion desde {addr}")
    t = Thread(target=handle_client, args=(conn, addr), daemon=True)
    t.start()
    _all_threads.append(t)
    try: t.join()
    except Exception as e:
        print("Error en el hilo:", e)
    return t

if __name__ == "__main__":
    print("""
        0. Salir
        1. Ver log
        2. Crear servidor local
    """)

    option = int(input("Elige una opcion: "))
    if option == 0:
        exit(0)
    elif option == 1:
        file = open("log.txt")
        print(file.read())
    elif option == 2:
        t = Thread(target=create_server, daemon=True)
        t.start()
        try:
            while True: 
                sleep(1)
        except KeyboardInterrupt:
            pass
    
    exit(0)
