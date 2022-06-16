import socket, threading

connections = []

def handle_user_connection(connection: socket.socket, address: str) -> None:

    while True:
        try:
            mensagemRecebidada = connection.recv(1024)

            if mensagemRecebidada:
                print(f'{address[0]}:{address[1]} - {mensagemRecebidada.decode()} ')
               
                mensagemRecebidadaEnviada = f'From {address[0]}:{address[1]} - {mensagemRecebidada.decode()}'
                broadcast(mensagemRecebidadaEnviada, connection)

            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break

def broadcast(mensagem: str, connection: socket.socket) -> None:
    
    for cliente in connections:
        if cliente != connection:
            try:
                cliente.send(mensagem.encode())

            except Exception as e:
                print(f'Erro ao enviar mensagem: {e}')
                remove_connection(cliente)

def remove_connection(conn: socket.socket) -> None:
    
    if conn in connections:
        conn.close()
        connections.remove(conn)

def server() -> None:

    LISTENING_PORT = 8000
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
        while True:

            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'{e}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()

if __name__ == "__main__":
    server()
    