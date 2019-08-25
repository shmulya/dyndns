# dyndns

Requirements:
apt install virtualenv, python3, python3-dev build-essential

Installing server:
1. cd /opt/
2. git clone https://github.com/shmulya/dyndns.git
3. virtualenv -p /usr/bin/python3 /opt/dyndns
4. cd /opt/dyndns
5. source bin/activate
6. pip install dnspython
7. pip install easyzone
8. pip install flask
9. pip install rsa
10. pip install uwsgi
11. mv easyzone.py lib/pythonYOUR_VERSION_HERE/site-packages/easyzone/
12. useradd -s /bin/false -G bind -d /opt/dyndns dyndns
13. mkdir rsa
14. mkdir client/rsa
15. chown -Rc dyndns:bind /opt/dyndns/
16. mv dyndns.service /etc/systemd/system/
17. systemctl start dyndns.service
18. Generating keys takes about 20-30 sec, after that you can stop service systemctl stop dyndns.service
19. cp public_server.pem client/rsa/public_server.pem
20. chown dyndns:dyndns client/rsa/public_server.pem

Installing client:
1. Copy client folder to remote server (/opt/dyndns-client/ by default)
2. pip3 install requests
3. pip3 install rsa
4. cd /opt/dyndns-client/
5. python3 client.py gen_rsa
6. edit client_config.py: domain - root domain, subdomains - subdomains to control
for example: domain = "example.com" subdomains = ["domain1", ""]. "" cname for root domain
7. get rsa/public.pem and put it to server rsa directory with domain as filename:
cp rsa/public /path/to/server/rsa/example.com
8. chmod g+w to your zonefile on server