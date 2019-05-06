#Name:__Joseph DAlessandro_____________________________________
#UCID:___21840023________________________________________________
#Class Section: ____Sec 102__


import time
import struct
from socket import *



# Basic structure from UDP server taken from Chapter 2 of textbook and class PowerPoint
#Information on how to use the socket methods from taken from https://docs.python.org/3/library/socket.html


def main():
    #set the server to the local IP
    serverIP= 'localhost'
    serverPort = 12000 #Sets the port the socket will use
    dataLength= 100000 #sets the size of the data
    count = 1 # keeps track of the sequence
    sent=0
    received=0
    lost=0.0
    
    listRTT = []

    clientSocket = socket(AF_INET, SOCK_DGRAM) #Creats the client socket
    
    
    print("Pinging " +  gethostbyname(serverIP)  + ", " + str(serverPort) + ": ") #Prints the server that is being pinged 
    
    
    while count <= 10: #Pings the server ten times
        
        data = (1, count) #Sets the data to be sent (Message type and the sequence number)
        packer = struct.Struct('i i')
        packed_data = packer.pack(*data)
        start = time.time() #From https://docs.python.org/2/library/time.html
        clientSocket.sendto(packed_data,(serverIP, serverPort)) # sends message
        sent+=1
        clientSocket.settimeout(0.01) #Set timeout to one sec from: https://docs.python.org/3/library/socket.html
        #Used exepting handeling as decribed in Python Programming by John Zelle along with socket timeout exeption
        try:
            
            dataEcho, address = clientSocket.recvfrom(dataLength)
            
            RTT = (time.time() - start)  #Find the round trip time
            
            listRTT.append(RTT) #adds to the list
            
            unpacker = struct.Struct('i i')
        
            message = unpacker.unpack(dataEcho) 
            
        
            print("Ping message number " + str(message[1]) + " RTT " + str(RTT) + " secs" )
            
            received+=1
         
        except timeout:
            
            print("Ping message number " + str(count) + " timed out" )
            lost+=1
            
            
            
                 
        count += 1 #increments the sequence number
        
    clientSocket.close()
    
    #Prints out the stats for the session
    pLost = (lost/sent)*100.0
    avgRTT= (sum(listRTT))/received #https://www.techwalla.com/articles/how-to-find-the-average-of-a-list-in-python
   
    print("Number of packets sent: " + str(sent))
    print("Number of packets received: " + str(received))
    print("Percent of packets lossed: " + str(pLost) + "%")
    print("The Minimum RTT was: " + str(min(listRTT)))
    print("The Maximum RTT was: " + str(max(listRTT)))
    print("The Average RTT was: " + str(avgRTT))
    
    
    
if __name__ == '__main__':
    main()
    
    
