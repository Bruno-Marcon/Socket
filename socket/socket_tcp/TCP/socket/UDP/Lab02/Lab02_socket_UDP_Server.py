import random
from socket import *

# Criar um socket UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

host = '127.0.0.1'
serverPort = 1200
# Atribuir endereço IP e número da porta ao socket
serverSocket.bind((host, 12000))

print("Servidor pronto para receber mensagens...")

while True:
    # Gerar número aleatório entre 0 e 10
    rand = random.randint(0, 10)
    
    # Receber o pacote do cliente junto com o endereço de origem
    message, address = serverSocket.recvfrom(1024)
    
    # Colocar a mensagem recebida em maiúsculas
    message = message.upper()
    
    # Se o número rand for menor que 4, consideramos que o pacote foi perdido e não respondemos
    if rand < 4:
        print(f"Simulando perda do pacote. Número aleatório: {rand}")
        continue
    
    # Enviar a mensagem de volta ao cliente
    serverSocket.sendto(message, address)
    print(f"Mensagem enviada para {address}: {message.decode()}")
