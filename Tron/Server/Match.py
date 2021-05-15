from .Engine import Engine
import queue

class Match:

    def __init__(self, matchID):
        self.clients = []
        self.commandQueue = queue.Queue()
        self.engine = Engine(self.clients, self.commandQueue)
        self.matchID = matchID
        #self.game = game

    def join(self, client):
        self.clients.append(client)
        client.assignQueue(self.commandQueue)
        #self.game.addPlayer(client.id)

    def stop(self):
        self.engine.stop()
        self.engine.join()

    def start(self):
        self.engine.start()

 