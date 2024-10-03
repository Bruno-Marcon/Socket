import time
from socket import *

# Endereço do servidor (substitua 'localhost' pelo IP do servidor se necessário)
host = '127.0.0.1'
serverPort = 1200

# Criar um socket UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Definir tempo limite para esperar a resposta (1 segundo)
clientSocket.settimeout(1)

# Enviar 10 pings para o servidor
for i in range(1, 11):
    # Obter o horário atual (início do ping)
    startTime = time.time()

    # Mensagem de ping
    message = f'Ping {i} {time.strftime("%H:%M:%S")}'

    try:
        # Enviar mensagem para o servidor
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        
        # Esperar resposta do servidor
        response, serverAddress = clientSocket.recvfrom(1024)

        # Obter o horário após o recebimento da resposta
        endTime = time.time()

        # Calcular RTT (Round Trip Time)
        rtt = endTime - startTime

        # Exibir o RTT e a resposta recebida
        print(f'Resposta do servidor: {response.decode()} | RTT: {rtt:.6f} segundos')

    except timeout:
        # Se o tempo limite for atingido, considerar que o pacote foi perdido
        print(f'Ping {i} - Pedido sem resposta (Timeout)')

# Fechar o socket
clientSocket.close()
