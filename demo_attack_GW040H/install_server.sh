#!/bin/bash

sudo apt update -y

sudo apt install tftp-hpa -y

echo -----------------------------------------------------------

cat /etc/default/tftpd-hpa | grep  TFTP_DIRECTORY 

echo -----------------------------------------------------------

sudo systemctl start tftpd-hpa.service

systemctl status tftpd-hpa.service


