#socket info = https://man7.org/linux/man-pages/man2/socket.2.html#top_of_page
#python specific socket package info = https://docs.python.org/3/library/socket.html
import socket
import random
import time
import datetime
import sys  #take in user input onn command line
import struct


#CLIENT SENDS INFO######### MEASURE THROUGHPUT ONN SERVER SIDE
#bigger than expected  receeive size  for udp
RECV_SIZE = 1050
HEADER_SIZE =  5
PACKET_PAYLOAD_SIZE = 1000

IP_addr  = "127.0.0.2"  #of server so it knows where to send the info
port =  1333

#DGRAM = udp type
ClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



##########################
#want to send  25-200 megabytes of data from the client to the server
#char = 1byte
num_Mbytes = sys.argv[1]

#convert to  num bytes = *10^6
tot_num_bytes = int(num_Mbytes)*1000000  
remaining_bytes = tot_num_bytes
rand_bytes_all = random.randbytes(tot_num_bytes)

seg_start = 0
seg_end = PACKET_PAYLOAD_SIZE

tot_time = 0
tot_payload_size = 0
bytes_sent = bytearray()
bytes_rec = bytearray()


while(remaining_bytes > 0):
    
    packet_size = PACKET_PAYLOAD_SIZE
    #0=no, 1=last packet
    is_last = 0

    if(remaining_bytes > PACKET_PAYLOAD_SIZE):
        remaining_bytes -= PACKET_PAYLOAD_SIZE
    else:
        remaining_bytes = 0
        packet_size = remaining_bytes
        is_last =  1

    #get the payload to send and record the sent bytes
    rand_bytes = rand_bytes_all[seg_start:seg_end]
    bytes_sent.extend(rand_bytes)
    seg_start += PACKET_PAYLOAD_SIZE
    seg_end += PACKET_PAYLOAD_SIZE

    #print timestamp if about to send the first packet
    if(remaining_bytes == tot_num_bytes - PACKET_PAYLOAD_SIZE):
        format_time_now = datetime.datetime.now()
        timestamp_now = format_time_now.strftime("%m/%d/%Y, %H:%M:%S")
        print("\nStart time stamp: ", timestamp_now)

    #return int of time
    #mod to get a number that is 30 bits = less than 4 bytes
    #also the necessary precision based on trial and error
    true_start_time = time.time_ns()
    start_time = true_start_time % 1000000000

    if(remaining_bytes == tot_num_bytes - PACKET_PAYLOAD_SIZE):
        print("Start time (ns since epoch): ", true_start_time)
    
    
    #sendto = no connection send = use with UDP?
    #(msg, addr to send to)
    #create address in geeneral as a tuple of host,port?
    #total bytes sent = 5 (time + whether this is last packet or not) + 1000 (payload)
    ClientSock.sendto((start_time.to_bytes(4,'big') + is_last.to_bytes(1, 'big') + rand_bytes), (IP_addr, port))



# tp_len +  throughput_bytes + ts_len + timestamp_end_bytes + cip_len +  client_ip_bytes + true_end_bytes
stats_data, serv_addr = ClientSock.recvfrom(RECV_SIZE)

tp_byte_len = stats_data[0]
start_ind =  tp_byte_len+1
throughput_bytes  = stats_data[1:start_ind]
ts_byte_len = stats_data[start_ind]
start_ind += 1
timestamp_end_bytes  = stats_data[start_ind:(start_ind+ts_byte_len)]
start_ind += ts_byte_len
cip_byte_len = stats_data[start_ind]
start_ind += 1
cip_bytes = stats_data[start_ind:(start_ind+cip_byte_len)]
start_ind += cip_byte_len
true_end = stats_data[start_ind:]


# print(int.from_bytes(timestamp_end_bytes, 'big'))

#print end time stamp
print("End time stamp: ", timestamp_end_bytes.decode('utf-8'))
print("End time (ns since epoch): ", int.from_bytes(true_end, 'big'))

print("\nThroughput in kB/sec: ", struct.unpack('f', throughput_bytes)[0])

#last data bytee =1 + data = 1000
data_received, serv_addr2 = ClientSock.recvfrom(RECV_SIZE)

while (data_received[0]  == 0):
    bytes_rec.extend(data_received[1:])
    data_received, serv_addr2 = ClientSock.recvfrom(RECV_SIZE)
if(data_received[0]  == 1):
    bytes_rec.extend(data_received[1:])

print("\nSize of data sent (MB): ", len(bytes_sent)/1000000)
print("Size of data received (MB): ", len(bytes_rec)/1000000)

print("\nClient IP: ", cip_bytes.decode('utf-8'))
print("Server IP: ", IP_addr, " ", port)

print("\nEach packet sent from client includes the time since epoch in ns right before the packet is sent, a byte that is 1 if it is the last packet the client wants to send (otherwise =0), and the payload data")
#print("\nData sent:\n ", bytes_sent)
#print("\n\n\n\n\nData received:\n", bytes_rec)




    
