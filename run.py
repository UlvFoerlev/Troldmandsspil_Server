from server.core.server import ServerCore

if __name__ == "__main__":
    core = ServerCore()

    with core():
        print("Connected by", core.addr)
        while True:
            data = core.conn.recv(1024)
            if not data:
                break
            core.conn.sendall(data)
