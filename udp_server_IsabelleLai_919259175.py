#socket info = https://man7.org/linux/man-pages/man2/socket.2.html#top_of_page
#python specific socket package info = https://docs.python.org/3/library/socket.html

# time modulee = https://docs.python.org/3/library/time.html 
import socket
import time
import datetime
import struct

#RECEIVES INFO, MEASURE THROUGHPUT AND SEND BACK TO CLIENNT
RECV_SIZE = 1050
HEADER_SIZE = 5

#addr and port =  way  to find each other on network
# google says  local host = ip addr of 127.0.0.1
#can use any port >1024?? randomly chosee 1333
IP_addr  = "127.0.0.2"
port =  1333
#create address in geeneral as a tuple of host,port?

#same socket type/setup as client 
ServSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServSock.bind((IP_addr, port))


tot_time = 0
tot_payload_size = 0
tot_data = bytearray()

while True:
    #use recvfrom() since it waits to receive before executing next code
    #recvfrom(num bytes of message), using 1050 bytes since it doesn't throw an error of
        #message too long for sendto in client socket file, and big enough to hold entire packet

    #data comes in msb->lsb: 4byte time, 1byte islast, 1000byte payload
    data, addr = ServSock.recvfrom(RECV_SIZE)
    true_end_time = time.time_ns()
    end_time = true_end_time % 1000000000

    is_last  = data[4]

    #get timestamp asap
    if(is_last == 1):
        format_time_end = datetime.datetime.now()

    #calculate elapsed time for each packet send
    start_time = int.from_bytes(data[:4], 'big')
    elapsed_time = end_time - start_time
    if(elapsed_time < 0):
        end_time = end_time + 1000000000
        elapsed_time = end_time - start_time
    
    #add to total elapsed time for the whole message to be sent
    tot_time += elapsed_time
    tot_payload_size += (len(data) - HEADER_SIZE)

    #record data received
    tot_data.extend(data[5:])

    if(is_last == 1): # the last packet

        timestamp_end = format_time_end.strftime("%m/%d/%Y, %H:%M:%S")
        timestamp_end_bytes = timestamp_end.encode('utf-8')  
        timestamp_end_b_len = len(timestamp_end_bytes)
        ts_len = timestamp_end_b_len.to_bytes(1, 'big')

        true_end_bytes = true_end_time.to_bytes(10, 'big')
    
        client_ip = str(addr[0]) +",  "+ str(addr[1])
        client_ip_bytes = client_ip.encode('utf-8') 
        client_ip_b_len = len(client_ip_bytes)
        cip_len = client_ip_b_len.to_bytes(1, 'big')

        #calculate throughput
        time_sec = float(tot_time)/(1000000000)
        payload_kb = float(tot_payload_size)/1000
        throughput = payload_kb/time_sec
        
        #puts into 4 bytes for 'f'
        throughput_bytes = struct.pack('f', throughput)
        throughput_b_len = len(throughput_bytes)
        tp_len = throughput_b_len.to_bytes(1, 'big')
        
        # tp_len,  ts_len = 1 byte
        ServSock.sendto((tp_len +  throughput_bytes + ts_len + timestamp_end_bytes + cip_len +  client_ip_bytes + true_end_bytes), addr)
        # print(throughput_bytes)
        # print(timestamp_end_bytes)
        # print(client_ip_bytes)
        # print(true_end_bytes)

        while(len(tot_data)>0):
            last_data = 0
            if(len(tot_data) <= 1000):
                last_data = 1
            ServSock.sendto(last_data.to_bytes(1, 'big') + tot_data[:1000], addr)
            del tot_data[:1000]
        exit()

