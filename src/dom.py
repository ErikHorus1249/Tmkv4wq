import scapy.all as scapy
import subprocess as sub
import re

#ans, unans = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst="192.168.1.62"),timeout=2)
#ans.summary(lambda s,r: r.sprintf("%Ether.src% %ARP.psrc%") )
ans,unans = scapy.arping("192.168.1.62",verbose=0)
ans.summary(lambda s,r: r.sprintf("%Ether.src% %ARP.psrc%") )
