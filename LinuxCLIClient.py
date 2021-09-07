import socket

def sendCommands(clientSocket):
    while True:
        request = input("Please enter a command: ")
        if len(request) == 0:
            print("Cannot send empty command")
            continue
        clientSocket.send(request.encode())
        reply = clientSocket.recv(4096).decode()
        if reply == "Error":
            print("Error, enter another command")
            continue
        elif reply == "Write":
            print("Enter message")
            print("To exit, type quit")
            while True:
                write = input("> ")
                if write == ("quit"):
                    clientSocket.send(write.encode())
                    break
                clientSocket.send(write.encode())
            reply = clientSocket.recv(4096).decode()
        elif reply == "Goodbye!":
            print(reply)
            clientSocket.close()
            break
        print(reply)

def main():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("192.168.192.161",9999))
    print(clientSocket.recv(4096).decode())
    sendCommands(clientSocket)

main()

