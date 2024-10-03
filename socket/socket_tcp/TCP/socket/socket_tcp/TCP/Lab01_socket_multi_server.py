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
            #Encerra conexão apos o cliente selecionar sair
            if message.strip().lower() == "exit":
                print(f"Cliente {client_id}: Solicitou encerramento da conexão.")
                break

            try:
                filename = message.split()[1]
                #Especifica o arquivo que o Client solicitou
                print(f"Cliente {client_id}: Fez requisição para '{filename[1:]}'")
                #Faz a busca do arquivo solicitado
                current_directory = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(current_directory, 'arquivos', filename[1:])
                #Abre o arquivo e coloca na variavel outputdata para ser enviado pelo socket
                with open(filepath, 'r') as f:
                    outputdata = f.read()
                #Confirma que foi realizado a conexão com sucesso ao Client
                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                #Realiza o envio do arquivo ao client
                connectionSocket.sendall(outputdata.encode())

                print(f"Cliente {client_id}: Resposta: {filename[1:]} enviada para o Cliente '{client_id} na porta: {addr[1]}'")

            except IOError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

                print(f"Cliente {client_id}: Arquivo '{filename[1:]}' não encontrado (404)")

    except BrokenPipeError:
        print(f"Cliente {client_id}: Conexão perdida.")

    finally:
        connectionSocket.close()
        print(f"Cliente {client_id}: Conexão encerrada.")
        print_lock.release()

def Main():
    global client_count
    host = '127.0.0.1'
    serverPort = 6788
    #Especifica para o SO qual o protocolo a ser utilizado, TCP ou UDP
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, serverPort))
    
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
