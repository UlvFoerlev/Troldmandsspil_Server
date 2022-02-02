from server.core.server import ServerCore

if __name__ == "__main__":
    core = ServerCore()

    with core() as s:
        while True:

            bytesAddressPair = s.recv(1024)
            if bytesAddressPair:
                print(bytesAddressPair)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)

            print(clientMsg)
            print(clientIP)
