import socket
import json

RECV_BYTES = 1050

serv_IP_addr = "127.0.0.3"
serv_port = 4448

ServSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ServSocket.bind((serv_IP_addr, serv_port))
ServSocket.listen(0)

try:
    while True:
        print("............................")
        ProxySocket, ProxyAddr = ServSocket.accept()

        #will always get a string (not json) from proxy
        packet_bytes = ProxySocket.recv(RECV_BYTES)

        message = packet_bytes.decode('utf-8')
        print("\nMessage received: ", message)    
    
        #send back to proxy
        response = ("RESPONSE||").encode('utf-8')
        response += packet_bytes

        print("Response to proxy: ", response.decode('utf-8'), "\n")
        ProxySocket.send(response)

        ProxySocket.close()

except KeyboardInterrupt:
    
    ServSocket.close()
    

