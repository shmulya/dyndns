import rsa
import requests
import json
import binascii
from sys import exit, argv
from client_config import URL, WORKDIR, domain, subdomains

try:
    pkeyfile = open(WORKDIR+'rsa/private.pem', 'r').read()
except Exception:
    (pubkey, pkey) = rsa.newkeys(2048, poolsize=4)
    open(WORKDIR+'rsa/private.pem', 'wb').write(pkey.save_pkcs1(format='PEM'))
    open(WORKDIR+'rsa/public.pem', 'wb').write(pubkey.save_pkcs1(format='PEM'))
    try:
        pubkeyfile = open(WORKDIR+'rsa/public_server.pem', 'r').read()
    except FileNotFoundError:
        print('Can\'t find public_server.pem')
        exit(1)
    else:
        pubkey = rsa.PublicKey.load_pkcs1(pubkeyfile)
else:
    pkey = rsa.PrivateKey.load_pkcs1(pkeyfile)
    try:
        pubkeyfile = open(WORKDIR+'rsa/public_server.pem', 'r').read()
    except FileNotFoundError:
        print('Can\'t find public_server.pem')
        exit(1)
    else:
        pubkey = rsa.PublicKey.load_pkcs1(pubkeyfile)

def gen_newkeys():
    (pubkey, pkey) = rsa.newkeys(2048, poolsize=4)
    open(WORKDIR + 'rsa/private.pem', 'wb').write(pkey.save_pkcs1(format='PEM'))
    open(WORKDIR + 'rsa/public.pem', 'wb').write(pubkey.save_pkcs1(format='PEM'))

def send_request(URL, enc_payload, signature):
    res = requests.post(URL, json={ 'message': binascii.b2a_base64(enc_payload).decode(),
                                    'signature': binascii.b2a_base64(signature).decode()
                                    })
    if res.status_code == 200:
        exit(0)
    else:
        print('Error')

def main():
    payload = {
         'domain': domain,
         'subdomains': subdomains
    }
    js = json.dumps(payload).encode('utf8')
    enc = rsa.encrypt(js, pubkey)
    signature = rsa.sign(js, pkey, 'SHA-256')
    send_request(URL, enc, signature)

if __name__ == '__main__':
    if argv[1] == 'gen_rsa':
        gen_newkeys()
        exit(0)
    else:
        main()