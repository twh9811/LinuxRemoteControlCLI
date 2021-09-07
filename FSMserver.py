from posixpath import split
import subprocess
import socket
import os

def userInput(clientSocket, clientAddress):
    comProcess = subprocess.run('pwd', shell=True, capture_output=True)
    currentDirectory = comProcess.stdout.decode().strip("\n")
    while True:
        clientRequestEncoded = clientSocket.recv(4096)
        clientRequestDecoded = clientRequestEncoded.decode()
        splitRequest = clientRequestDecoded.split(" ") 
        #Must support..
        #PWD
        if splitRequest[0] == "pwd":
            comProcess = subprocess.run('pwd', shell=True, capture_output=True, cwd=currentDirectory)
            workingDirectory = comProcess.stdout
            print("Working directory has been sent")
            clientSocket.send(workingDirectory)
        #ls
        elif splitRequest[0] == "ls":
            comProcess = subprocess.run('ls', shell=True, capture_output=True, cwd=currentDirectory)
            currentContents = comProcess.stdout
            line = currentContents.decode()
            if len(line) == 0:
                print("Empty directory sent")
                clientSocket.send("Empty directory...".encode())
            else:    
                print("Current Contents of directory has been sent")
                clientSocket.send(currentContents)
        #mkdir <arg>
        elif splitRequest[0] == "mkdir":
            if os.path.isdir(splitRequest[1]):
                print("Directory already exists")
                clientSocket.send("Directory already exists".encode())
            else:
                comProcess = subprocess.run(['mkdir', splitRequest[1]],cwd=currentDirectory)
                print("Created the directory: " + splitRequest[1])
                clientSocket.send((splitRequest[1] + ": directory created.").encode())
        # #write<path>
        elif splitRequest[0] == "write":
            os.chdir(currentDirectory)
            try:
                if os.path.exists(splitRequest[1]):
                    print("That file already exists.")
                    clientSocket.send("That file exists already".encode())
                else:
                    f = os.open(splitRequest[1], os.O_RDWR|os.O_CREAT)
                    clientSocket.send("Write".encode())
                    while True:
                        line = clientSocket.recv(4096).decode() + "\n"
                        if line == 'quit' + "\n":
                            break
                        print("Added line to file")
                        os.write(f, line.encode())
                    os.close(f)
                    print("File saved")
                    clientSocket.send("File saved".encode())
            except FileNotFoundError:
                clientSocket.send("File/Directory doesn't exist".encode())
        #cat<path>  
        elif splitRequest[0] == "cat":
            os.chdir(currentDirectory)
            if os.path.exists(splitRequest[1]):
                print("Reading file...")
                comProcess = subprocess.run(['cat', splitRequest[1]], capture_output=True)
                fileContents = comProcess.stdout
                print("Sending data...")
                clientSocket.send(fileContents)    
            else:
                print("That file does not exist.")
                clientSocket.send("That file does not exist. Try again.".encode())
        #cd<dir>
        elif splitRequest[0] == "cd":
            if os.path.exists(splitRequest[1]):
                print("Changing into directory " + splitRequest[1])
                currentDirectory = splitRequest[1]
                clientSocket.send("Changed folder".encode())
            else:
                print("Directory doesn't exist")
                clientSocket.send("Cannot change into that directory. Try again".encode())
        #quit
        elif splitRequest[0] == "quit":
            print("Closed connection from " + str(clientAddress))
            clientSocket.send("Goodbye!".encode())
            clientSocket.close()
            break
        else:
            print("Invalid command, please try again.")
            clientSocket.send("Error".encode())


def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("192.168.192.161", 9999))
    print("Server is running...")

    serverSocket.listen(3)
    while True:
        clientSocket,clientAddress = serverSocket.accept()
        print("New connection from: ", clientAddress)
        clientSocket.send("You've been connected to the server.".encode())
        userInput(clientSocket, clientAddress)

main()