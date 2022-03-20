*Before executing the code you need to make neceessary changes in the source code.
*Some changes depend on the operation system you are using.

default admin login creds : Username - admin or Admin
                    Password - admin123

[Windows]
    1.Change the ip on server.py[line 93] & client.py[line 17] to your local ip. (Use command 'ipconfig' on cmd.)
    2.On Windows machine, in both server.py[line 91] and client.py[line 15] rewrite it to --> os.system("cls")
[Linux distros & Termux]
    1.Change the ip on server.py[line 93] & client.py[line 17] to your local ip. (Use command 'ifconfig' on terminal.)
