import threading
import socket
from .Client import Client
from .MatchList import MatchList

class ServerListener(threading.Thread):

    def __init__(self, socket):
        super().__init__()
        self.clientList = []
        self.socket = socket
        self.running = True
        self.idCount = 0
        self.matchList = MatchList()

    def run(self):

        while self.running:
            try:
                clientFD, addr = self.socket.accept()
                print(f"""Connection accepted from {addr}""")
                client = Client(clientFD, self.matchList, self.idCount)
                self.idCount += 1
                client.start()
                self.clientList.append(client)
            except:
                break

    def orderlyShutdown(self):
        for client in self.clientList:
            client.shutdown()
            client.join()

    def shutdown(self):
        self.running = False
        self.orderlyShutdown()
        self.matchList.shutdown()
        
