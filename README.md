
增加自定义服务器列表支持，请将服务器地址列表放在同文件夹下，文件名： list.txt
格式:

	8.8.8.8:8499
	4.4.4.4:8499
	#1.1.1.1:8849

暂时不使用的服务器地址可使用#注释
-----------

本程序fork自shadowsocks。增加对多个服务端的支持，如果在限制带宽的内网使用，可达到多倍带宽的效果。在下载http资源，及播放在线视频时有显著加速功能。

I forked this  project, and try to update it so it can connect to multi-servers, so I can use more bandwidth,
I hope it can take effects, ^_~

2012.4.21 00:00
-----------
shadowsocks
===========

shadowsocks is a lightweight tunnel proxy which can help you get through firewalls


usage
-----------

Put `server.py` on your server. Edit `server.py`, change the following values:

    PORT          server port
    KEY           a password to identify clients

Run `python server.py` on your server. To run it in the background, run `setsid python server.py`.

Put `local.py` on your client machine. Edit `local.py`, change these values:

    SERVER  your  your server ip or hostname
    REMOTE_PORT   server port
    PORT          local port
    KEY           a password, it must be the same as the password of your server

Run `python local.py` on your client machine.

Change proxy settings of your browser into

    SOCKS5 127.0.0.1:PORT
