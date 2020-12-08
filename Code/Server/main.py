import io
import os
import socket
import time
import picamera
import sys, getopt
from pi_thread import *
from threading import Thread
from server import Server

class SmartCarServer():
    
    def __init__(self):
        self.TCP_Server = Server()
        
    def open(self):
        self.TCP_Server.StartTcpServer()
        self.ReadData = Thread(target=self.TCP_Server.readdata)
        self.SendVideo = Thread(target=self.TCP_Server.sendvideo)
        self.power = Thread(target=self.TCP_Server.Power)
        self.SendVideo.start()
        self.ReadData.start()
        self.power.start()
                
    def close(self):
        stop_thread(self.SendVideo)
        stop_thread(self.ReadData)
        stop_thread(self.power)

        self.TCP_Server.server_socket.shutdown(2)
        self.TCP_Server.server_socket1.shutdown(2)
        self.TCP_Server.StopTcpServer()
            
if __name__ == '__main__':
    s = SmartCarServer()
    try:
        s.open()
    except KeyboardInterrupt:
        s.close()
