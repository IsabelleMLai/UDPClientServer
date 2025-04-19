import socket
#JSON format = converting info  into formatted string
import json
#give 4 letter string in commannd line
import sys

RECV_BYTES = 1050

proxy_IP = "127.0.0.4"
proxy_port = 3333
serv_IP = "127.0.0.3"
serv_port = 4448

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#useful:
#https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python 
ClientSocket.connect((proxy_IP, proxy_port))

message = sys.argv[1]
print("............................")

print("\nMessage to send: ",  message)
#{} = dictionary
data = {
    "server_ip": serv_IP, 
    "server_port": serv_port, 
    "message": message #TCHANGE TO ACTUAL MESSAGE
}
print("JSON data: ", data)
json_format = json.dumps(data)
packet_bytes = json_format.encode('utf-8')

ClientSocket.send(packet_bytes)
print("..............")


#connection was shutdown,  proxy will not send anything else 
#happens when proxy gets the message 
msg_sent  = ClientSocket.recv(RECV_BYTES)
print("Message received:  ", msg_sent.decode('utf-8'), "\n")
print("............................")

ClientSocket.close()
exit()

