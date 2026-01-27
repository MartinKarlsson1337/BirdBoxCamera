
The camera is on 192.168.1.X

Commands for switching network (in elevated cmd):
netsh interface ipv4 set address name="Ethernet" static 192.168.1.69 255.255.255.0
netsh interface ipv4 set address name="Ethernet" dhcp 192.168.0.69 255.255.255.0
