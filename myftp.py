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
    command = "PASV" + "\r\n"
    # Complete
    
    clientSocket.sendall(command.encode("utf-8"))  #turns my commands into bytes and talks to server

    data = receiveData(clientSocket) #stores erver responses into data var
    
    status = 0
    
    dataSocket = socket(AF_INET, SOCK_STREAM) #create connection for ftp
    
    if data.startswith("227"):
        status = 227
        # Complete
        
        left = data.find("(")   #decode server pasv response algo for ip and port
        right = data.find(")")
        numbers = data[left+1:right].split(",")

        ip = numbers[0] + "." + numbers[1] + "." + numbers[2] + "." + numbers[3]
        port = (int(numbers[4]) * 256) + int(numbers[5])
        
        dataSocket.connect((ip, port))
        
    return status, dataSocket
    
def receiveAllBytes(dataSocket): #recieving data for get
    file_bytes = b""
    while True:
        chunk = dataSocket.recv(4096)
        if not chunk:
            break
        file_bytes += chunk
    return file_bytes
    
    
def main():
    # COMPLETE

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP socket
    # COMPLETE
    HOST = sys.argv[1] #stores server in a var
    clientSocket.connect((HOST, 21))


    # COMPLETE
    
    dataIn = receiveData(clientSocket)
    print(dataIn)

    status = 0
    dataSocket = None #placeholder for creating the var

    
    if dataIn.startswith("220"): #server greeting check 220
        status = 220
        print("Sending username")
        # COMPLETE
        
        command = "USER " + username + "\r\n" #sending user commandn
        clientSocket.sendall(command.encode("utf-8")) 
        dataIn = receiveData(clientSocket) 
        
        print(dataIn)

        print("Sending password")
        if dataIn.startswith("331"): #asking for password
            status = 331
            # COMPLETE
            
            command = "PASS " + password + "\r\n" #sending pass command
            clientSocket.sendall(command.encode("utf-8")) 
            dataIn = receiveData(clientSocket) 
            
            print(dataIn)
            if dataIn.startswith("230"): #login success check
                status = 230

       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE

        while True:
            user_input = input("myftp> ")

            if user_input == "ls": #ls functionality
                pasvStatus, dataSocket = modePASV(clientSocket)

                if pasvStatus != 227:
                    print("Failure")
                else:
                    command = "LIST" + "\r\n"
                    clientSocket.sendall(command.encode("utf-8"))

                    reply = receiveData(clientSocket)

                    if reply.startswith("150") or reply.startswith("125"):
                        listing_text = ""
                        while True:
                            chunk = dataSocket.recv(4096)
                            if not chunk:
                                break
                            listing_text += chunk.decode("utf-8", errors="ignore")

                        dataSocket.close()

                        final_reply = receiveData(clientSocket)

                        print(listing_text)

                        if final_reply.startswith("226"):
                            print("Success")
                        else:
                            print("Failure")
                    else:
                        dataSocket.close()
                        print("Failure")

            elif user_input.startswith("cd "): #cd functionality
                remote_dir = user_input.split(" ", 1)[1].strip()

                command = "CWD " + remote_dir + "\r\n"
                clientSocket.sendall(command.encode("utf-8"))

                reply = receiveData(clientSocket)

                if reply.startswith("250"):
                    print("Success")
                else:
                    print("Failure")

            elif user_input.startswith("get "): #get functionality
                # COMPLETE
                remote_filename = user_input.split(" ", 1)[1].strip()

                pasvStatus, dataSocket = modePASV(clientSocket)

                if pasvStatus != 227:
                    print("Failure")
                else:
                    command = "RETR " + remote_filename + "\r\n"
                    clientSocket.sendall(command.encode("utf-8"))

                    reply = receiveData(clientSocket)

                    if reply.startswith("150") or reply.startswith("125"):
                        total_bytes = 0
                        with open(remote_filename, "wb") as output_file:
                            while True:
                                chunk = dataSocket.recv(4096)
                                if not chunk:
                                    break
                                output_file.write(chunk)
                                total_bytes += len(chunk)

                        dataSocket.close()
                        dataSocket = None

                        final_reply = receiveData(clientSocket)

                        if final_reply.startswith("226"):
                            print("Success")
                            print(str(total_bytes) + " bytes transferred")
                        else:
                            print("Failure")
                    else:
                        dataSocket.close()
                        dataSocket = None
                        print("Failure")

            elif user_input.startswith("put "): #put functionality
                local_filename = user_input.split(" ", 1)[1].strip()

                try:
                    input_file = open(local_filename, "rb")
                except:
                    print("Failure")
                else:
                    pasvStatus, dataSocket = modePASV(clientSocket)

                    if pasvStatus != 227:
                        print("Failure")
                    else:
                        command = "STOR " + local_filename + "\r\n"
                        clientSocket.sendall(command.encode("utf-8"))

                        reply = receiveData(clientSocket)

                        if reply.startswith("150") or reply.startswith("125"):
                            total_bytes = 0

                            while True:
                                chunk = input_file.read(4096)
                                if not chunk:
                                    break
                                dataSocket.sendall(chunk)
                                total_bytes += len(chunk)

                            input_file.close()
                            dataSocket.close()

                            final_reply = receiveData(clientSocket)

                            if final_reply.startswith("226"):
                                print("Success")
                                print(str(total_bytes) + " bytes transferred")
                            else:
                                print("Failure")
                        else:
                            input_file.close()
                            dataSocket.close()
                            print("Failure")

            elif user_input.startswith("delete "): #delete functionality
                remote_filename = user_input.split(" ", 1)[1].strip()

                command = "DELE " + remote_filename + "\r\n"
                clientSocket.sendall(command.encode("utf-8"))

                reply = receiveData(clientSocket)

                if reply.startswith("250"):
                    print("Success")
                else:
                    print("Failure")

            elif user_input == "quit": #quit functionality
                command = "QUIT" + "\r\n"
                clientSocket.sendall(command.encode("utf-8"))

                reply = receiveData(clientSocket)

                if reply.startswith("221"):
                    print("Success")
                else:
                    print("Failure")

                break

    print("Disconnecting...")
    
    clientSocket.close()
    if dataSocket is not None: #datasocket check
        dataSocket.close()
    
    sys.exit() #Terminate the program after sending the corresponding data

main()

