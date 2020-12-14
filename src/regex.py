import re

str = '192.168.1.76'
match = re.search(r'192.168.[0123456789]+', str)
if match: #nếu tồn tại chuỗi khớp                     
    print (match.group()) # in ra chuỗi đó
else:
    print ('Khong tim thay!') # Không thì hiện thông báo