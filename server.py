#include <ethernet.h>
import socket
import threading
import logging
import logging.handlers
from collections import deque
import pcapy
import sys
import datetime
from struct import *

my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address="/dev/log")
my_logger.addHandler(handler)

def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (a[0] , a[1] , a[2], a[3], a[4], a[5])
    return b

def parse_packet(packet) :

    eth_length = 14
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    my_logger.debug('Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))
    print('Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))


    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]

        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        my_logger.debug('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))
        print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))

#TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]

            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4

            my_logger.debug('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))
            print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))

            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size

            #get data from the packet
            data = packet[h_size:]
            print("Data: ", data)
            my_logger.debug(data)

# ICMP Packets
        elif protocol == 1:
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u + 4]
            icmph = unpack('!BBH', icmp_header)
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
            print('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum))
            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) - h_size
            data = packet[h_size:]

            print("Data: ", data)
            my_logger.debug(data)

# UDP packets
        elif protocol == 17:
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u + 8]
            udph = unpack('!HHHH', udp_header)
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
            print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                length) + ' Checksum : ' + str(checksum))
            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size
            data = packet[h_size:]

            print("Data: ", data)
            my_logger.debug(data)

# some other IP packet like IGMP
        else:
            print('Protocol other than TCP/UDP/ICMP')
            my_logger.error('Protocol other than TCP/UDP/ICMP')

        print


def game(white, black):

    white.send(bytes('You are white', 'utf-8'))
    black.send(bytes('You are black', 'utf-8'))
    while True:

        (header,packet) = cap.next()
        my_logger.debug('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
        print('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))

        parse_packet(packet)
        white_move = white.recv(4096)
        my_logger.debug(f"White's move: {white_move}")
        if white_move.decode('utf-8') == 'lost':
            break
        black.send(white_move)
        black_move = black.recv(4096)
        my_logger.debug(f"Black's move: {black_move}")
        if black_move.decode('utf-8') == 'lost':
            break
        white.send(black_move)


def get_interface():
    ifs = pcapy.findalldevs()
    if 0 == len(ifs):
        my_logger.error("You don't have enough permissions to open any interface on this system.")
        sys.exit(1)
    elif 1 == len(ifs):
        my_logger.debug('Only one interface present, defaulting to it.')
        return ifs[0]
    count = 0
    for i in ifs:
        print(f'nr.{count} Int: {i}')
        count += 1
    idx = int(input('Please select number of the interface, which you want to sniff : '))
    return ifs[idx]


if __name__ == '__main__':
    dev = get_interface()
    queue = deque([])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6789))
    s.listen()
    cap = pcapy.open_live(dev, 65536, 1, 0)

    while True:
        conn, address = s.accept()
        #################################
        my_logger.debug(f'Connection from {address} accepted')
        conn.send(bytes('You are in queue', 'utf-8'))
        queue.append(conn)
        if len(queue) >= 2:
            threading.Thread(group=None, target=game, args=(queue.popleft(), queue.popleft())).start()
