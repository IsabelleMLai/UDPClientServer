#configured multiple loopback  addresses on mac os in terminal
    #   =  $ sudo ifconfig lo0 alias 127.0.0.4 up
    #do every single address you want to add

import socket
import json

RECV_BYTES = 1050

proxy_IP = "127.0.0.4"
proxy_port = 3333


server_IP_blocklist = ["127.0.0.5"]

ProxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


ProxySocket.bind((proxy_IP, proxy_port))
#wait for someone  to try and send something 
# will always listen if you keeep this socket ProxySocket open
ProxySocket.listen(2)

try:
    while  True:
        print("............................")
        #accept connection,  take in message = packet_bytes
        ClientSocket, ClientAddr = ProxySocket.accept()
        
        packet_bytes = ClientSocket.recv(RECV_BYTES)

        #make a sender socket each time you want  to send something
        ServSocket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        json_format = packet_bytes.decode('utf-8')
        data  = json.loads(json_format)
        print("\nData received from client in JSON format: ", json_format)

        #pull out IP to go to, forward packeet theree
        serv_IP = data["server_ip"]
        serv_port = data["server_port"]
        serv_data_str = data["message"]
        serv_data_bytes =  serv_data_str.encode('utf-8')
        
        #use sending sockeet to send the data to server
        ServSocket.connect((serv_IP, serv_port))
        server_ip, server_port = ServSocket.getpeername()
        if(server_ip in server_IP_blocklist):
            #error, sennd error message to client only
            error_message  = "Error ip in blocklist"
            print("Sending error message to client: ", error_message)

            ClientSocket.send(error_message.encode('utf-8'))
            ClientSocket.close()
            # SendingSocket.shutdown?
        else:
            #otherwise forward meessage to server and get response
            print("Sending message to server: ", serv_data_str)
            ServSocket.send(serv_data_bytes)
            print("..............")

            serv_response = ServSocket.recv(RECV_BYTES)
            print("Message received from server, forwarding to client: ", serv_response.decode('utf-8'), "\n")
            ClientSocket.send(serv_response)

            ServSocket.close()
            ClientSocket.close()

except KeyboardInterrupt:
    ProxySocket.close()
    
