import socket
import sys
from .ServerListener import ServerListener



class Server:

    def __init__(self, HOST, PORT):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((HOST, PORT))
            self.socket.listen()
        except:
            raise Exception("Unable to create socket")

        self.serverListener = ServerListener(self.socket)

    def run(self):

        self.serverListener.start()
        cont = " "

        while cont != "q":
            cont = input(" ")

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.serverListener.shutdown()
        self.serverListener.join()

    

