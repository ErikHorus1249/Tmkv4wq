#!/bin/bash

# host ip
host="192.168.1.39"
# port 
port="2000"

#notify
echo "[+]Starting . . ."
echo "[+]Downloading . . ."

# download file from host
busybox tftp -g -r tcpdump $host
echo "[!]Downloaded tcpdump"
busybox tftp -g -r busybox-mips $host

# authornization
chmod 777 *
echo "[!]Downloaded busybox-mips"
echo "[+]Start getting Pcap infomation"

# get pcap and send to host
./tcpdump -i  br0 | ./busybox-mips nc -w3 $host $port

echo "Done !"
