#Name:__Joseph D'Alessandro_____________________________________
#UCID:___21840023________________________________________________
#Class Section: ____Sec 102__

import random
import struct
import time
from socket import *

# Basic structure from UDP server taken from Chapter 2 of textbook and class PowerPoint
#Information on how to use the socket methods from taken from https://docs.python.org/3/library/socket.html

def main(): 
    
    #set the server to the local IP
    serverIP= "localhost"
    serverPort = 12000 #Sets the port the socket will use
    dataLength= 100000 #Set the size of the data 
    
    serverSocket = socket(AF_INET, SOCK_DGRAM) #Creats the UDP Socket
    
    serverSocket.bind((serverIP, serverPort)) #binds the socket to the port

    
    print('The server is ready to receive on port: ' + str(serverPort))
                      
    while True: #uses a while loop to receive incoming datagram and randomly drop some
        
        rand = random.randint(0,10) #generates a random number
        
        data, address = serverSocket.recvfrom(dataLength) #Reads the socket and gets the message and address
        
        #information about using struct from https://pymotw.com/2/socket/binary.html
        unpacker = struct.Struct('i i')
        
        message = unpacker.unpack(data) 
          
        
        if rand < 4: #Drops the message if random is less then 4
            print("Message with sequence number " + str(message[1]) + " dropped")
            continue
        #Sets the return message
        data = (2, message[1]) #Sets the data to be sent (Message type and the sequence number)
        packer = struct.Struct('i i')
        pData = packer.pack(*data)
         
        #https://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string-in-python
        print("Responding to ping request with sequence number " + str(message[1]) ) #Prints that it is responding to the message
        time.sleep(0.001) #some packets work recording 0.0secs so I had to pad the time
        serverSocket.sendto(pData,address) 
        

if __name__ == '__main__':
    main()
