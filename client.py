import socket 
import _thread

data = ""
  
class SimpleTcpClient():
    
    def __init__(self):  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('10.254.0.37',5555))
        self.running = True
            
    def send(self, msg):
        msg = msg.encode()
        self.sock.send(msg)
        
    def startListenerForServer(self):
        _thread.start_new_thread(self.receive, ())
        
    def receive(self):
        global data
        
        while self.running:
            try:
                msg = self.sock.recv(1024)
                msg = msg.decode()
                data = msg
            except:
                print("conn failed")
    
    def close(self):
        self.running = False
        self.sock.close()
        
#for test purpose
if __name__ == "__main__":
    socket = SimpleTcpClient()
    
    while True:        
        msg = str(input("TESTT:"))
        socket.send(msg)
        print(data)