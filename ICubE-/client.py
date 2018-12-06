import socket
import threading
import gui

server_ip = '127.0.0.1'
server_port = 51742
banned_letters_in_nickname = "`~!@#$%^&*()-=+[]{}\\|;:'\",<.>/? "
status = 0      # 0: before game start, 1: error, 2: game started

# WIP


def alert_connection_error():
    global status
    gui.AlertConnectionErrorGui().show()
    status = 1


def select_nickname():
    global my_socket

    nickname = gui.ChooseNicknameGui(banned_letters=banned_letters_in_nickname).show()
    try:
        my_socket.send(bytes(nickname, 'utf-8'))
    except ConnectionError:
        alert_connection_error()
        return


def select_room():
    global my_socket

    try:
        data = my_socket.recv(1024)
    except ConnectionError:
        alert_connection_error()
        return
    room_names = eval(data.decode('utf-8'))
    selected_room = gui.ChooseRoomGui(rooms=room_names).show()
    try:
        my_socket.send(bytes(selected_room, 'utf-8'))
    except ConnectionError:
        alert_connection_error()
        return


def receive():
    global my_socket
    global status

    while status == 0:
        try:
            data = my_socket.recv(1024)
        except ConnectionError:
            alert_connection_error()
            return
        if data.decode('utf-8') == "$gameStarted":
            status = 2
            print("please enter once")
        else:
            print(data.decode('utf-8'))


def receive_tmp():
    global my_socket
    global status

    while True:
        try:
            data = my_socket.recv(1024)
        except ConnectionError:
            alert_connection_error()
            return
        print(data.decode('utf-8'))


def send():
    global my_socket

    while status == 0:
        s = input('> ')
        try:
            my_socket.send(bytes(s, 'utf-8'))
        except ConnectionError:
            alert_connection_error()
            return


def connect():
    global my_socket

    while True:
        select_nickname()
        if status == 1:
            return
        select_room()
        if status == 1:
            return
        while True:
            r = threading.Thread(target=receive, args=())
            c = threading.Thread(target=send, args=())
            r.start()
            c.start()
            r.join()
            c.join()
            if status == 1:
                return
            elif status == 2:
                break
        while True:
            r = threading.Thread(target=receive_tmp, args=())
            c = threading.Thread(target=send, args=())
            r.start()
            c.start()
            r.join()
            c.join()
            if status == 1:
                return


server_address = (server_ip, server_port)

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.connect(server_address)
except ConnectionRefusedError:
    print("서버가 응답하지 않습니다.")
    quit()

connect()

my_socket.close()
