import socket
import time
import os

op = 0
helpp = ' For basic arithmatics, Usage - [operand1][operator][operand2] eg 2+2 or 6/3...\n\
 Other commands,\n\
  1.exit       --Log out of current session.\n\
  2.end        --End the current session(Closes the client program.)\n\
  3.Terminate  --Shut the server down(Requires administration access).\n\
  4.clear      --Clear the output screen'

def validate(username,cli_sock):
    cli_sock.send(bytes('Enter Passwd : ','utf-8'))
    try:
        passwd = cli_sock.recv(1024)
    except KeyboardInterrupt as k:
        flag = 'Terminate'
        print('  [OK]Force Stop!')
        return flag
    if passwd.decode('utf-8') == 'admin123':
        cli_sock.send(bytes('Authentication Sucessfull.','utf-8'))
        return 'auth'
    else:
        cli_sock.send(bytes('Authentication Unsucessfull.','utf-8'))
        print("  [.]Admin Authentication unsuccessfull.")
        return 'unauth'

def saviour(cli_msg,op):
    for x in cli_msg:
        if x == "+" or x == "-" or x == "*" or x == "/":
            op = x       
    if op == 0:
        return 0,0,0
    elif op == '+'or op == "-" or op == "*" or op == "/":
        li = list(cli_msg.split(op))
        op1 = li[0]
        op2 = li[1]

        try:
            v = int(op1)
            vv= int(op2)
        except ValueError as V:
            return 0,0,0

        return op,op1,op2    

def exception(cli_msg,flag,username):
    if cli_msg == 'exit':
        close = 'Adios...'
        cli_sock.send(bytes(close,'utf-8'))
        print("  [.]Closed")
        flag ='exit'
        return flag
    if cli_msg == 'end':
        close = 'Session Terminated.'
        cli_sock.send(bytes(close,'utf-8'))
        print("  [.]Closed")
        flag='end'
        return flag
    if cli_msg == 'help' or cli_msg == '?':
        cli_sock.send(helpp.encode('utf-8'))
        flag = 'helpp'
        return flag
        
    if cli_msg == 'Terminate':
        if username == 'Admin' or username == 'admin':
            confirmation = 'Are you sure you want to shutdown the server?(y/n) : '
            cli_sock.send(bytes(confirmation,'utf-8'))
            confirmation = cli_sock.recv(1024).decode('utf-8')
            if confirmation == 'y':
                close = 'Bye Admin.'
                cli_sock.send(bytes(close,'utf-8'))
                print("  [.]Closed")
                print('[-]Shutting Server down.')
                cli_sock.close()
                time.sleep(0.5)
                s.close()
                print('\n[OK]Server down.')
                flag ='Terminate'
                return flag
            elif confirmation == 'n':
                flag = 'not_terminate'
                return flag
        else:
            close = 'Unauthorised command.'
            cli_sock.send(bytes(close,'utf-8'))
            flag = 'unauth_user'
            return flag
        
os.system("clear") 

ip = '192.168.0.11'
port = 5000
error =  'Ambigious command.'

print("-" * 50)
print(f"Creating a server socket... {ip}:{port}")
time.sleep(1)
print("Done setting up the port.")
print("-" *50)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

try:
    s.bind((ip,port))
except OSError as o:
    print("Port occupied. Don't press Ctrl+z you idiot. Use Ctrl+c insted.\nChange the port number form source code (server & client both) & Try again.")
    exit()

s.listen(5)

time.sleep(2)
while True:
    flag = ''
    if flag == '':
        print("[*]Waiting for the hosts to connect...")

    try:
        cli_sock,cli_add = s.accept()
    except KeyboardInterrupt as k:
        print('\n[OK]Force Stop!')
        break

    try:
        username = cli_sock.recv(1024) 
    except KeyboardInterrupt as k:
        print("Force Stop!")
        break
    if not username:
        print('  [.]Connection terminated unexpectedly.')
        continue

    username = username.decode('utf-8')

    if username == 'Admin' or username == 'admin':
        print(f"  [.]{username} login authenticating.")
        flag = validate(username,cli_sock)

    if flag == 'unauth':
        continue
    if flag == 'Terminate':
        break

    print(f"  [.]{username} logged in.")
    time.sleep(1)
    msg = f"Welcome to the server {username}"

    cli_sock.send((bytes(msg,'utf-8'))) 
    
    while True:
        try:
            cli_msg = cli_sock.recv(1024)
        except KeyboardInterrupt as k:
            print('\n  [OK]Force Stop!')
            flag = 'Terminate'
            break

        cli_msg = cli_msg.decode('utf-8')

        flag = exception(cli_msg,flag,username)

        if flag == 'helpp':
            continue
        if flag == 'exit':
            break
        if flag == 'end':
            break
        if flag == 'unauth_user':
            continue
        if flag == 'not_terminate':
            continue
        if flag == 'Terminate':
            break
        
        operation,op1,op2 = saviour(cli_msg,op)

        try:
            if operation == 0 :
                cli_sock.send(bytes('Ambiguos command.','utf-8'))
                continue
        except BrokenPipeError as B:
            print('  [.]Connection terminated unexpectedly.')
            break

        op1 = int(op1)
        op2 = int(op2)
        
        if operation == '+':
            res = op1+op2
        if operation == '-':
            res = op1-op2
        if operation == '*':
            res = op1*op2
        if operation == '/':
            if op2 == 0:
                res = 'Invalid input.'
                cli_sock.send((bytes(res,'utf-8')))
                continue
            else:
                res = op1/op2
        res = f'{op1}{operation}{op2}={res}'    
        cli_sock.send((bytes(res,'utf-8')))
    if flag == 'Terminate':
        break
s.close()

