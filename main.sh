#!/bin/bash  

MAC=$(arp -a)
echo "$MAC" > result.txt
file='./result.txt'
while IFS= read line
do
    result='['
    ip=( $(grep -Eo '\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' <<<"$line"))
    mac=( $(grep -Eo '\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$\b' <<<"$line") )
    if [ -z "$mac" ];
    then
        continue
    else
        echo 'ip :' "$ip" 'MAC' "$mac"
    fi
done <"$file"
rm ./result.txt
