import socket
import _thread

#init socket
seversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind socket to port

#ip address need to changed
seversocket.bind(('10.254.0.37', 5555))

#create listner
seversocket.listen(0)

#save connections
connections = []

#create data buffer
data = []
#save wether running
running = True

#save index
index = 0

#listener for client
def client_thread(conn, index):
    global data
    global running
    
    #main loop
    while running:
        try:
            #receive message
            msg = conn.recv(1024)
            msg = msg.decode()
            #update buffer
            data[index] = msg
        except:
            break
    
    #close connection
    conn.close()

#listener for server
def server_thread():
    global index
    global running
    global data
    
    #main loop
    while running:
        #search for incoming connection
        conn, acc = seversocket.accept()
        connections.append(conn)
        #extend data buffer
        data.append("")
        #create new listner
        _thread.start_new_thread(client_thread, (conn,index))
        index += 1

    socket_close()

def send(msg, conn):
    
    try:
        msg = msg.encode()
        conn.send(msg)
    except OSError:
        connections.remove(conn)

#start server
def start():
    _thread.start_new_thread(server_thread, ())

#test main
if __name__ == '__main__':
    start()
    
    while True:
        print(data)

#close socket  
def socket_close():
    seversocket.close() 