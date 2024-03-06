import constants
import socket
import threading

clients_sockets=[]
clients_sockets_lock=constants.UNLOCKED
def open_socket():
    server_running=True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((constants.SERVER_IP, constants.SERVER_PORT))
    server.listen(constants.MAX_QUEUE_LENGTH)

    while server_running:
        communication_socket=server.accept()[0]
        clients_sockets.append(communication_socket)

        if len(clients_sockets)>=2 and clients_sockets_lock==constants.UNLOCKED:
            clients_sockets_lock=constants.LOCKED
            thread=threading.Thread(target=start_game_between_2_players, args=[])
            thread.start()
            thread.join()
            clients_sockets_lock=constants.UNLOCKED


    return #the socket

def start_game_between_2_players():
    player_1_socket=clients_sockets.pop()
    player_2_socket=clients_sockets.pop()

    game_running=True

    player_1_socket.send(constants.START_GAME)
    player_2_socket.send(constants.START_GAME)

    while game_running:
        message_from_board1 = player_1_socket.recv(1024)
        message_from_board2 = player_2_socket.recv(1024)

        response_to_player_1 = chose_response_to_message_during_game(message_from_board2)
        response_to_player_2 = chose_response_to_message_during_game(message_from_board1)

        if response_to_player_1[0]!=constants.SEND_BOARD or response_to_player_2[0]!=constants.SEND_BOARD:
            game_running=False

        player_1_socket.send(response_to_player_1.encode())
        player_2_socket.send(response_to_player_2.encode())

    player_1_socket.close()
    player_2_socket.close()



def chose_response_to_message_during_game(message):
    message_list=message.split(" ")

    message_code=message_list[0]
    other_player_board=message_list[1]
    is_other_player_eating_apple=message_list[2]

    match message_code:
        case constants.WON_GAME:
            return constants.LOST_GAME

        case constants.LOST_GAME:
            return constants.WON_GAME

        case constants.SEND_BOARD:
            return constants.SEND_BOARD+" "+other_player_board+" "+is_other_player_eating_apple
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