import constants
import socket
import threading
import dbmanager
import time

clients_sockets_searching_for_game_queue=[]
clients_sockets_queue_lock=constants.UNLOCKED

def handle_client(client_socket):
    clients_request=''
    while clients_request!=constants.REQUEST_GAME:
        clients_request=client_socket.recv(1024).decode()
        response_to_send=chose_response_to_message(clients_request)
        client_socket.send(response_to_send.encode())

    added_to_search_queue=False
    while added_to_search_queue==False:
        if clients_sockets_lock == constants.UNLOCKED:
            clients_sockets_lock = constants.LOCKED
            clients_sockets_searching_for_game_queue.append(client_socket)
            added_to_search_queue=True
            clients_sockets_lock = constants.UNLOCKED
        else:
            time.sleep(constants.WAIT_TIME)

def open_socket():
    server_running=True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((constants.SERVER_IP, constants.SERVER_PORT))
    server.listen(constants.MAX_QUEUE_LENGTH)

    while server_running:
        communication_socket=server.accept()[0]

        thread=threading.Thread(target=handle_client, args=[communication_socket])
        thread.start()
        thread.join()

        if len(clients_sockets_searching_for_game_queue)>=2:
            while clients_sockets_lock==constants.LOCKED:
                time.sleep(constants.WAIT_TIME)
            clients_sockets_lock=constants.LOCKED
            thread=threading.Thread(target=start_game_between_2_players, args=[])
            thread.start()
            thread.join()
            clients_sockets_lock=constants.UNLOCKED



def start_game_between_2_players():
    player_1_socket=clients_sockets_searching_for_game_queue.pop()
    player_2_socket=clients_sockets_searching_for_game_queue.pop()

    game_running=True

    player_1_socket.send(constants.START_GAME)
    player_2_socket.send(constants.START_GAME)

    while game_running:
        message_from_board1 = player_1_socket.recv(1024).decode()
        message_from_board2 = player_2_socket.recv(1024).decode()

        response_to_player_1 = chose_response_to_message_during_game(message_from_board2)
        response_to_player_2 = chose_response_to_message_during_game(message_from_board1)

        if response_to_player_1[0]!=constants.SEND_BOARD or response_to_player_2[0]!=constants.SEND_BOARD:
            game_running=False

        player_1_socket.send(response_to_player_1.encode())
        player_2_socket.send(response_to_player_2.encode())

    thread = threading.Thread(target=handle_client, args=[player_1_socket])
    thread.start()
    thread.join()

    thread2 = threading.Thread(target=handle_client, args=[player_2_socket])
    thread2.start()
    thread2.join()



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

def chose_response_to_message(message):
    response=''
    message=message.split()
    match message[0]:
        case constants.REGISTER:
            response=dbmanager.register(message[1],message[2])
        case constants.LOGIN:
            response=dbmanager.login(message[1],message[2])
        case constants.GET_STATS:
            response=dbmanager.get_stats(message[1])

    return response



open_socket()