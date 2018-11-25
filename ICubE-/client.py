import socket
import threading

server_ip = '127.0.0.1'
server_port = 51742

# WIP


def connect():
    global my_socket

    while True:
        print("10자 이하의 닉네임을 입력하세요.")
        while True:
            try:
                nickname = input("> ")
            except KeyboardInterrupt:
                continue
            try:
                my_socket.send(bytes(nickname, 'utf-8'))
            except ConnectionError:
                print("접속이 비정상적으로 종료되었습니다.")
                return
            try:
                data = my_socket.recv(1024)
            except ConnectionError:
                print("접속이 비정상적으로 종료되었습니다.")
                return
            sys_msg = data.decode('utf-8')
            if sys_msg == "$confirmNickname":
                break
            elif sys_msg == "$tooLongNickname":
                print("닉네임이 너무 깁니다. 10자 이하로 입력하세요.")
            else:
                print("닉네임에 특수문자를 사용할 수 없습니다.")

        try:
            data = my_socket.recv(1024)
        except ConnectionError:
            print("접속이 비정상적으로 종료되었습니다.")
            return
        room_names = eval(data.decode('utf-8'))
        print("게임방 목록")
        for room_name in room_names:
            print(room_name)
        print("들어갈 게임방의 이름을 입력하세요.")
        print("목록에 없는 이름이 입력되면 그 이름으로 게임방을 생성합니다.")
        while True:
            while True:
                try:
                    selected_room = input('> ')
                    break
                except KeyboardInterrupt:
                    continue
            if selected_room in room_names:
                print("{} 게임방에 들어가는 것이 맞습니까?(Y/N)".format(selected_room))
            else:
                print("{} 게임방을 생성하는 것이 맞습니까?(Y/N)".format(selected_room))
            # response = ""
            while True:
                try:
                    response = input('> ')
                except KeyboardInterrupt:
                    continue
                if not (response.upper().startswith('Y') or response.upper().startswith('N')):
                    continue
                else:
                    break
            if response.upper().startswith('Y'):
                break
            else:
                continue
        try:
            my_socket.send(bytes(selected_room, 'utf-8'))
        except ConnectionError:
            print("접속이 비정상적으로 종료되었습니다.")
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
