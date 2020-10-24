def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


import socket, select, datetime

HEADER_LENGTH = 10  # Sets the chat size limit to 10 MB
IP = '127.0.0.1'  # The standard IP address
PORT = 1234  # Sets the port number; the more random, the better

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

while True:  # Runs the main loop forever until you exit
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_adress = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f'\n{user["data"].decode("utf-8")} joined the chatroom\n')  # Prints that a user joined the chat

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f'\n{clients[notified_socket]["data"].decode("utf-8")} has left the chatroom\n')  # Prints that someone left the chat
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'{user["data"].decode("utf-8")} {datetime.datetime.now().strftime("%d/%m/%Y at %H:%M:%S")}\n{message["data"].decode("utf-8")}\n')  # Prints the recieved message

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
