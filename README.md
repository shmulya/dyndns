# dyndns

Requirements:
```
apt install virtualenv, python3, python3-dev build-essential
```

Installing server (from root):
1. git clone https://github.com/shmulya/dyndns.git /opt/dyndns
2. cd /opt/dyndns
3. python3 setup.py
4. cp public_server.pem client/rsa/public_server.pem
5. chown dyndns:dyndns client/rsa/public_server.pem

```
systemclt start dyndns - start service
systemclt stop dyndns - stop service
systemclt restart dyndns - restart service 
/var/log/dyndns.log - log
```

Installing client:
1. Copy client folder to remote server (/opt/dyndns-client/ by default)
2. pip3 install requests
3. pip3 install rsa
4. cd /opt/dyndns-client/
5. python3 client.py gen_rsa
6. edit client_config.py: 
```
URL - server's usr. http://your_ip:12227/domain
domain - root domain 
subdomains - subdomains to control for example: 
domain = "example.com" 
subdomains = ["domain1", ""]. 
"" - cname for root domain (@, example.com., etc.)
```
7. get rsa/public.pem and put it to server rsa directory with domain as filename:
```
cp rsa/public /path/to/server/rsa/example.com
```
8. chmod g+w to your zonefile on server
