import constants
import socket

clients_sockets=[]
def open_socket():
    server_running=True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((constants.SERVER_IP, constants.SERVER_PORT))
    server.listen(constants.MAX_QUEUE_LENGTH)
    while server_running:
        communication_socket=server.accept()[0]
        clients_sockets.append(communication_socket)
        
        message_from_client = communication_socket.recv(1024).decode('utf-8')
        communication_socket.send(f"message received".encode('utf-8'))
        print(message_from_client)

    print('what')





    return #the socket
def main():
    open_socket()
    m=constants.REGISTER
    chose_response_to_message("hi")

def chose_response_to_message(message):
    match message[0]:
        case constants.REGISTER:
            register_user(message[1],message[2])
        case constants.LOGIN:
            login_user(message[1],message[2])
def register_user(username,password):
    return constants.SUCCESS

def login_user(username,password):
    return constants.SUCCESS

open_socket()