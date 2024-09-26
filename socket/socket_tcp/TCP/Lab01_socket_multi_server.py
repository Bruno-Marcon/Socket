import socket
from _thread import *
import threading
import sys
import os

print_lock = threading.Lock()

client_count = 0

def handle_client(connectionSocket, addr, client_id):
    try:
        while True:
            message = connectionSocket.recv(1024).decode()

            if message.strip().lower() == "exit":
                print(f"Cliente {client_id}: Solicitou encerramento da conexão.")
                break

            try:
                filename = message.split()[1]
                
                print(f"Cliente {client_id}: Fez requisição para '{filename[1:]}'")

                current_directory = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(current_directory, 'arquivos', filename[1:])

                with open(filepath, 'r') as f:
                    outputdata = f.read()

                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                
                connectionSocket.sendall(outputdata.encode())

                print(f"Cliente {client_id}: Resposta enviada para '{filename[1:]}'")

            except IOError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

                print(f"Cliente {client_id}: Arquivo '{filename[1:]}' não encontrado (404)")

    except BrokenPipeError:
        print(f"Cliente {client_id}: Conexão perdida (Broken Pipe).")

    finally:
        connectionSocket.close()
        print(f"Cliente {client_id}: Conexão encerrada.")
        print_lock.release()

def Main():
    global client_count
    serverPort = 6789
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(5)
    print(f'Server is listening on port {serverPort}')

    while True:
        connectionSocket, addr = serverSocket.accept()
        
        client_count += 1

        print_lock.acquire()
        print(f'Cliente {client_count}: Conectado a {addr[0]} : {addr[1]}')

        start_new_thread(handle_client, (connectionSocket, addr, client_count))

    serverSocket.close()

if __name__ == '__main__':
    Main()
