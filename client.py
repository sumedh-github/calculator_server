import socket
import time
import os
import subprocess

protected_users = ['Admin']
user_list = {'Admin'}

def design(ip,port):
    print("-" * 50)
    print("Creating a client socket...")
    print(f"Connecting to {ip}:{port}")
    print("(*)Sucessful")
    print("-" * 50)
    print('* Note-Username login is not mandatory. Its just for log purpose\n\
       Press ENTER for Guest login or just enter your name.\n\
       After logging in enter cmd "help" or "?" For more info...')

os.system("clear")

ip = '192.168.0.11'
port = 5001
print("-" * 50)
print("Creating a client socket...")
time.sleep(1)
print(f"Connecting to {ip}:{port}")
print("(*)Sucessful")
print("-" * 50)
time.sleep(1)

flag = False

print('* Note-Username login is not mandatory. Its just for log purpose\n\
       Press ENTER for Guest login or just enter your name.\n\
       After logging in enter cmd "help" or "?" For more info...')
time.sleep(2)


while True:
    flag2 = ''

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    try:
        s.connect((ip,port))
    except ConnectionRefusedError as c:
        print('[-]Server Not Found.')
        break

    try:
        username = input("Username : ")
    except KeyboardInterrupt as k:
        print('\nForced stop!')
        break

    if username == '' or username == 'guest':
        username = 'Guest'
    if username == 'admin':
        username = 'Admin'
    user_list.add(username)
    username = username.encode('utf-8')
    s.send(username)
    
    for user in protected_users:
        if user == 'Guest':
            break
        if user == username.decode('utf-8'):
            passpr = s.recv(1024).decode('utf-8')
            print(passpr)
            if passpr == 'Enter Passwd : ':
                try:
                    passwd = input("--> ")
                except KeyboardInterrupt as k:
                    print('Force Stop!')
                    s.send(bytes('null','utf-8'))
                    auth_ack = s.recv(1024).decode('utf-8')
                    print('[' + auth_ack + ']')
                    print('\n')
                    flag2 = 'save'
                    break
                if passwd == '':
                    s.send(bytes('null','utf-8'))
                    auth_ack = s.recv(1024).decode('utf-8')
                    print('[' + auth_ack + ']')
                    print('\n')
                    flag2 = 'save'
                    break
                    
                s.send(passwd.encode('utf-8'))
                auth_ack = s.recv(1024).decode('utf-8')
                if auth_ack == 'Authentication Sucessfull.':
                    print('[' + auth_ack + ']')
                    print('\n')
                    break
                else :
                    print('[' + auth_ack + ']')
                    print('\n')
                    flag2 = 'save'
                    break

    if flag2 == 'save':
        continue
    msg = s.recv(1024)

    while True:
        if username.decode('utf-8') == 'Admin' or username.decode('utf-8') == 'admin':
            print(f"{username.decode('utf-8')}@Server-[#] ",end=" ")
        else:
            print(f"{username.decode('utf-8')}@Server-[@] ",end=" ")

        try:
            msg = input()
        except KeyboardInterrupt as k:
            flag = True
            print('\nForced stop!')
            break

        if msg == '':
            continue

        if msg == 'clear':
            os.system('clear')
            design(ip,port)
            continue
        if msg[:5] == 'psswd':
            protected_users.append(username.decode('utf-8'))
        if msg == 'show users':
            if username.decode('utf-8') == 'Admin':
                for x in user_list:
                    print(x)
                continue
            else:
                print('Unauthorised command.')
                continue
        
        msg = msg.encode("utf-8")

        try:
            s.send(msg)
        except BrokenPipeError as b:
            print('Server Not Responding...')
            break

        res = s.recv(1024)
        print(res.decode('utf-8'))

        if msg.decode('utf-8') == 'help' or msg.decode('utf-8') == '?':
            print('\n')
            continue
        if res.decode('utf-8') == 'Adios...':
            print("\n")
            s.close()
            break
        if res.decode('utf-8') == 'Session Terminated.':
            s.close()
            exit()
            break
        if res.decode('utf-8') == 'Password changed sucessfully.':
            continue
        if res.decode('utf-8') == 'Cant set a password on {username} account.':
            protected_users.remove('Guest')
            continue
        if res.decode('utf-8') == 'Are you sure you want to shutdown the server?(y/n) : ':
            try:
                confirmation = input()
            except KeyboardInterrupt as k:
                print("Force Stop!")
                continue
            if confirmation == 'y':
                s.send(confirmation.encode('utf-8'))
                s.recv(1024) 
                s.close()
                exit()
            elif confirmation == 'n':
                s.send(confirmation.encode('utf-8'))
                continue
            else :
                print('Invalid input.')
                continue
            break
        if res.decode('utf-8') == 'Unauthorised command.':
            continue
        if res.decode('utf-8') == 'Ambigious command.':
            continue
    if flag:
        break
