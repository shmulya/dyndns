# dyndns

Requirements:
apt install virtualenv, python3, python3-dev build-essential

Installing server:
1. sudo python3 setup.py
2. cp public_server.pem client/rsa/public_server.pem
3. chown dyndns:dyndns client/rsa/public_server.pem

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
