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
10. mv easyzone.py lib/pythonYOUR_VERSION_HERE/site-packages/easyzone/
11. useradd -s /bin/false -G bind -d /opt/dyndns dyndns
12. chown -Rc dyndns:bind /opt/dyndns/
13. mv dyndns.service /etc/systemd/system/
14. systemctl start dyndn.service
15. 