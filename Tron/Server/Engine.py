import threading, queue

class Engine(threading.Thread):

    def __init__(self, clients, commandQueue):
        super().__init__()
        self.clients = clients
        self.notifications = queue.Queue()
        self.commandQueue = commandQueue
        self.running = True
        #self.game = game

    def run(self):
        notifThread = threading.Thread(target=self.sendNotif)
        notifThread.start()

        self.popCommands()
        notifThread.join()

    def stop(self):
        self.running = False
        self.commandQueue.put(None)
    
    def popCommands(self):

        while self.running:
            message =  self.commandQueue.get()
            if message is not None:
                print(message)

    def sendNotif(self):
        pass
