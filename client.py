import socket, threading

def handle_messages(connection: socket.socket):
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f': saiu do chat')
            connection.close()
            break

def cliente() -> None:
    
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 8000

    try:
        clienteSocket = socket.socket()
        clienteSocket.connect((SERVER_ADDRESS, SERVER_PORT))

        threading.Thread(target=handle_messages, args=[clienteSocket]).start()

        print('Conectado ao chat.')

        while True:
            msg = input()
            if msg == 'sair':
                print('Saindo do chat.')
                break

            clienteSocket.send(msg.encode())

        clienteSocket.close()

    except Exception as e:
        print(f'Erro: {e}')
        clienteSocket.close()

if __name__ == "__main__":
    cliente()
