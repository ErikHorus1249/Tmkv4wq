# Create your tasks here
from __future__ import absolute_import, unicode_literals
# from celery import shared_task
# from IoTAnalyzer.celery import app
from typing import Any, List
# from celery import shared_task
# from devices.models import Devices
import nmap
import socket
import re
# from pyroute2 import IPRoute
from scapy.all import *
# from IoTAnalyzer import config
 
 
# @shared_task
# def publish_message(message):
#     with app.producer_pool.acquire(block=True) as producer:
#         producer.publish(
#             message,
#             exchange=config.RabbitMQ_Config['exchange'],
#             routing_key=config.RabbitMQ_Config['routing_key'],
#         )
 
 
# @shared_task
def arp_scan(ip):
    """
    Performs a network scan by sending ARP requests to an IP address or a range of IP addresses.
 
    Args:
        ip (str): An IP address or IP address range to scan. For example:
                    - 192.168.1.1 to scan a single IP address
                    - 192.168.1.1/24 to scan a range of IP addresses.
 
    Returns:
        A list of dictionaries mapping IP addresses to MAC addresses. For example:
        [
            {'IP': '192.168.2.1', 'MAC': 'c4:93:d9:8b:3e:5a'}
        ]
    """
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
 
    ans, unans = srp(request, timeout=2, retry=1)
    result = []
 
    for sent, received in ans:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})
 
    return result
 
 
# @shared_task
def getLocalIPv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
 
    local_ip = (s.getsockname()[0])
    return local_ip
 
 
# @shared_task
def getNetworkInfo():
    local_ip = getLocalIPv4()
    ip = IPRoute()
    list_interfaces_detail = [{'iface': x['index'],'addr': x.get_attr('IFA_ADDRESS'),'mask': x['prefixlen']} for x in ip.get_addr()]
    result = None
    for x in list_interfaces_detail:
        if (x['addr'] == local_ip):
            result = x
    print(result)
    ip.close()
    return result
 
 
# @shared_task
# def scanDevices(ip_range: str, port_range: str) -> Any:
 
#     nmScan = nmap.PortScanner()
 
#     local_ip = getLocalIPv4()
#     if not ip_range:
#         ip_range = re.sub(r"\.([^.]*)$", ".*", local_ip)
 
#     result: Any = nmScan.scan(ip_range, port_range)
#     return result
 
 
# @shared_task
# def add(x, y):
#     return x + y
 
 
# @shared_task
# def mul(x, y):
#     return x * y
 
 
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
 
 
# @shared_task
# def count_devices():
#     return Devices.objects.count()
 
 
# @shared_task
# def get_devices():
#     return Devices.objects.all()
 
 
# @shared_task
# def rename_widget(device_id, name):
#     w = Devices.objects.get(id=device_id)
#     w.name = name
# w.save()

if __name__ == "__main__":
    # victim ip address
    target = "192.168.1.31"
    print arp_scan(target)
