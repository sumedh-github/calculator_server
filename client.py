import socket
import time
import os

def design(ip,port):
    print("-" * 50)
    print("Creating a client socket...")
    print(f"Connecting to {ip}:{port}")
    print("(*)Sucessful")
    print("-" * 50)
    print('* Note-Username login is not mandatory. Its just for log purpose\n\
    Press ENTER for Guest login or just enter your name,it doesnt really matter.\n\
    After logging in enter cmd "help" or "?" For more info...\n')

os.system("clear")

ip = '192.168.0.11'
port = 5000
print("-" * 50)
print("Creating a client socket...")
time.sleep(1)
print(f"Connecting to {ip}:{port}")
print("(*)Sucessful")
print("-" * 50)
time.sleep(1)

flag = False

print('* Note-Username login is not mandatory. Its just for log purpose\n\
    Press ENTER for Guest login or just enter your name,it doesnt really matter.\n\
    After logging in enter cmd "help" or "?" For more info...\n')

while True:
    time.sleep(2)

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

    if username == '':
        username = 'Guest'
    
    username = username.encode('utf-8')
    s.send(username) 
    
    if username.decode('utf-8') == 'Admin' or username.decode('utf-8') == 'admin':
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
                continue
            if passwd == '':
                s.send(bytes('null','utf-8'))
                auth_ack = s.recv(1024).decode('utf-8')
                print('[' + auth_ack + ']')
                print('\n')
                continue
                
            s.send(passwd.encode('utf-8'))
            auth_ack = s.recv(1024).decode('utf-8')
            if auth_ack == 'Authentication Sucessfull.':
                print('[' + auth_ack + ']')
                print('\n')
            else :
                print('[' + auth_ack + ']')
                print('\n')
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
        if res.decode('utf-8') == 'Are you sure you want to shutdown the server?(y/n) : ':
            try:
                confirmation = input()
            except KeyboardInterrupt as k:
                print("Force Stop!")
                continue
            if confirmation == 'y':
                s.send(confirmation.encode('utf-8'))
                s.recv(1024) #Bye sumedh.
                s.close()
                exit()
            elif confirmation == 'n':
                s.send(confirmation.encode('utf-8'))
                continue
            break
        if res.decode('utf-8') == 'Unauthorised command.':
            continue
        if res.decode('utf-8') == 'Ambigious command.':
            continue
    if flag:
        break
