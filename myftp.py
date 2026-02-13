# Help: https://www.eventhelix.com/networking/ftp/
# Help: https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf
# Help: https://realpython.com/python-sockets/
# Help: PASV mode may be easier in the long run. Active mode works 
# Reading: https://unix.stackexchange.com/questions/93566/ls-command-in-ftp-not-working
# Reading: https://stackoverflow.com/questions/14498331/what-should-be-the-ftp-response-to-pasv-command

#import socket module
from socket import *
import sys # In order to terminate the program

def quitFTP(clientSocket):
    # COMPLETE
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut)
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    print(data)

def sendCommand(socket, command):
    dataOut = command.encode("utf-8")
    # Complete
    return data



def receiveData(clientSocket):
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

# If you use passive mode you may want to use this method but you have to complete it
# You will not be penalized if you don't
def modePASV(clientSocket):
    # Sabrina appends "\r\n" on her branch so no need to add here
    sendCommand(clientSocket, "PASV")
    data = receiveData(clientSocket)
    print(data)

    status = 0
    dataSocket = None

    if data.startswith("227"):
        try:
            left = data.index("(")
            right = data.index(")", left)
            parts = data[left + 1:right].split(",")

            h1, h2, h3, h4, p1, p2 = [int(part.strip()) for part in parts]
            ip = f"{h1}.{h2}.{h3}.{h4}"
            port = p1 * 256 + p2

            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.connect((ip, port))
            status = 227
        except Exception:
            status = 0
            dataSocket = None

    return status, dataSocket


def ftpList(clientSocket):
    pasvStatus, dataSocket = modePASV(clientSocket)
    if pasvStatus != 227 or dataSocket is None:
        print("PASV failed")
        return

    # LIST triggers data transfer
    sendCommand(clientSocket, "LIST")

    # reply before data transfer
    resp1 = receiveData(clientSocket)
    print(resp1)

    # Read listing from socket until server closes it
    chunks = []
    while True:
        chunk = dataSocket.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)

    dataSocket.close()

    listing = b"".join(chunks).decode("utf-8", errors="replace")
    print(listing, end="" if listing.endswith("\n") else "\n")

    # Completion message
    completionReply = receiveData(clientSocket)
    print(completionReply)


def ftpDelete(clientSocket, filename):
    if not filename:
        print("Usage: delete <filename>")
        return

    # Sabrina appends \r\n in sendCommand()
    sendCommand(clientSocket, "DELE " + filename)

    resp = receiveData(clientSocket)
    print(resp)

    
def main():
    # COMPLETE
    # Initialize to prevent crash
    dataSocket = None

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP socket
    # COMPLETE

    HOST = # COMPLETE
    # COMPLETE

    dataIn = receiveData(clientSocket)
    print(dataIn)

    status = 0
    
    if dataIn.startswith(""):
        status = 220
        print("Sending username")
        # COMPLETE
        
        print(dataIn)

        print("Sending password")
        if dataIn.startswith(""):
            status = 331
            # COMPLETE
            
            print(dataIn)
            if dataIn.startswith(""):
                status = 230

       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        # pasvStatus, dataSocket = modePASV(clientSocket)
        # if pasvStatus == 227:
            # COMPLETE
        while True:
            userInput = input("myftp> ").strip()
            if not userInput:
                continue

            parts = userInput.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd == "ls":
                ftpList(clientSocket)
            elif cmd == "delete":
                ftpDelete(clientSocket, arg)
            elif cmd == "quit":
                quitFTP(clientSocket)
                break
            else:
                print("Command not implemented...")

    
    print("Disconnecting...")
    

    clientSocket.close()
    if dataSocket is not None:
        dataSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

main()

