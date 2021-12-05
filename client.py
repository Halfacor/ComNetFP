# python 3.9.9
import sys
import re
from socket import *
# ref: textbook examples

# get udpserver, udpport and hawkid from argv
_, UDPServerHostName, UDPServerPort, YourHawkID, *_ = sys.argv
UDPServerPort = int(UDPServerPort)
print(
    f"UDPServerHostName: {UDPServerHostName}, UDPServerPortNum: {UDPServerPort}, HawkID: {YourHawkID} \n")

# create UDP socket
clientUDPsocket = socket(AF_INET, SOCK_DGRAM)
print("UDP socket created with IPv4")
# send data with UDP datagram
clientUDPsocket.sendto(YourHawkID.encode(),
                       (UDPServerHostName, UDPServerPort))
print(f"UDP data sent: {YourHawkID}")
# get TCP server info from UDP server responses
udpResponse, _ = clientUDPsocket.recvfrom(2048)
print("UDP response received \n")
clientUDPsocket.close()

# extract tcp server address and port number for next part
tcpInfo = udpResponse.decode()
TCPServerHostName, TCPServerPort = tcpInfo.split(' ')
TCPServerPort = int(TCPServerPort)
print(
    f"TCPServerHostName: {TCPServerHostName}, TCPServerPort: {TCPServerPort}")

# create TCP socket
clientTCPsocket = socket(AF_INET, SOCK_STREAM)
print("TCP socket created with IPv4")
clientTCPsocket.connect((TCPServerHostName, TCPServerPort))
print("TCP connection established!")
clientTCPsocket.send("hello".encode())
print("TCP data sent: hello")
quited = False

while not quited:
    tcpResponse = clientTCPsocket.recv(1024)
    print("TCP data received: " + tcpResponse.decode())
    msgToSend = input("Next message to send? ")
    if (tcpResponse.decode()[1] == '4') and (msgToSend == "quit"):
        print("closing connection, goodbye")
        clientTCPsocket.close()
        quited = True
    else:
        clientTCPsocket.send(msgToSend.encode())
        print(f"TCP data sent: {msgToSend}")


print("Done")
