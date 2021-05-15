import socket
import threading

class Client(threading.Thread):

    def __init__(self, socket, matchList, id):
        super().__init__()
        self.socket = socket
        self.running = True
        self.matchList = matchList
        self.commandQueue = None
        self.id = id

    def receive(self, size):
        return self.socket.recv(size)

    def _processEvents(self):
        if self.commandQueue is None:
            raise Exception("Player must first join a match.")

        while self.running:
            message = self.socket.recv(1).decode()
            self.commandQueue.put(message)

    def run(self):
        #matchId = self.socket.recv(2).decode()
        self.matchList.create(self)
        if self.commandQueue is None:
            raise Exception("Player must first join a match.")

        while self.running:
            message = self.socket.recv(1).decode()
            self.commandQueue.put(message)
        

    def assignQueue(self, queue):
        self.commandQueue = queue

    def shutdown(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

