## TFTP
**Trivial File Transfer Protocol**  **(TFTP)** là một [giao thức truyền tập tin](https://vi.wikipedia.org/wiki/FTP "FTP") đơn giản theo bước, cho phép một khách hàng download một tập tin từ hoặc upload một tập tin vào một [máy chủ](https://vi.wikipedia.org/wiki/M%C3%A1y_ch%E1%BB%A7 "Máy chủ") từ xa. 
### Main Features

-   File transfer :
	- **GET** : download file from server 
	- **PUT** : Upload file from client to server 
### In case of used
#### 1. Install TFTP server for linux :
$ sudo  apt update

![](https://linuxhint.com/wp-content/uploads/2019/05/1-8.png)

The APT package repository cache should be updated.

![](https://linuxhint.com/wp-content/uploads/2019/05/2-8.png)

Now, install the  **tftpd-hpa**  package with the following command:
$ sudo  apt  install  tftpd-hpa

![](https://linuxhint.com/wp-content/uploads/2019/05/3-8.png)

**tftpd-hpa**  package should be installed.

![](https://linuxhint.com/wp-content/uploads/2019/05/4-8.png)

Now, check whether the  **tftpd-hpa**  service is running with the following command:

$ sudo  systemctl status tftpd-hpa

![](https://linuxhint.com/wp-content/uploads/2019/05/5-7.png)


**TFTP_DIRECTORY**  is set to  **/var/lib/tftpboot**. It means  **/var/lib/tftpboot** is the directory on this server which you will be able to accessing via TFTP.

**TFTP_ADDRESS**  is set to  **:69**. It means TFTP will run on port  **69**.

**TFTP_OPTIONS**  is set to  **–secure**. This variable sets the TFTP options. There are many options that you can use to configure how the TFTP server will behave. I will talk about some of them later. The  **–secure** option means change the TFTP directory to what is set on the  **TFTP_DIRECTORY**  variable when you connect to the TFTP server automatically. This is a security feature. If you hadn’t set the  **–secure**  option, then you would have to connect to the TFTP server and set the directory manually. Which is a lot of hassle and very insecure.

![](https://linuxhint.com/wp-content/uploads/2019/05/8-7.png)
#### 2. Busybox :
Command :

   For downloading from server.

>  $ busybox tftp -g -r filename [host]

    
    -g : get mode 
    -r : remote file 
    -filename : file's name is stored in server 
    -host : IP address of server 


**Reference :**
- **[wikipedia](https://vi.wikipedia.org/wiki/Trivial_File_Transfer_Protocol)** 
- **[linuxhint](https://linuxhint.com/install_tftp_server_ubuntu/)**

