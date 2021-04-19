import random

Encoding = input("Choose endoing from UTF-8, UTF-16BE, UTF32BE")
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(Encoding).strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


import socket, select, datetime

HEADER_LENGTH = input("Choose Chat size limit between 10 - 50 MB")  # Sets the chat size limit to 10 - 50 MB
IP = input("Enter IP Address")  # Choose the IP Address
PORT = random.randint(1000,9999) # Sets the port number; the more random, the better

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
            print(f'\n{user["data"].decode(Encoding)} joined the chatroom\n')  # Prints that a user joined the chat

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f'\n{clients[notified_socket]["data"].decode(Encoding)} has left the chatroom\n')  # Prints that someone left the chat
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'{user["data"].decode(Encoding)} {datetime.datetime.now().strftime("%d/%m/%Y at %H:%M:%S")}\n{message["data"].decode("utf-8")}\n')  # Prints the recieved message

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
