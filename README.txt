*V1.3 Optional password protection for any user.
[Bugs\UnderDev] :Guest should be password free anyhow.[DEV]
                 Admin should have a default password.[FIXED]
                 Welcome to the server[*BUG].[FIXED]

default admin login creds : Username - admin or Admin
                            Password - admin123
                 
*Before executing the code you need to make neceessary changes in the source code.
*Some changes depend on the operation system you are using.

[Windows]
    1.Change the ip on server.py[line 93] & client.py[line 17] to your local ip. (Use command 'ipconfig' on cmd.)
    2.On Windows machine, in both server.py[line 91] and client.py[line 15] rewrite it to --> os.system("cls")
[Linux distros & Termux]
    1.Change the ip on server.py[line 93] & client.py[line 17] to your local ip. (Use command 'ifconfig' on terminal.)
