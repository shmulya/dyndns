from flask import Flask, request
import rsa
import json
import binascii
from easyzone import easyzone
from easyzone.zone_reload import ZoneReload
from config import ZONEDIR, WORKDIR, LISTEN


app = Flask(__name__, static_url_path='')
try:
     pkeyfile = open(WORKDIR+'private_server.pem', 'r').read()
except Exception:
     print('Can\'t find RSA server keys. Generating...')
     (pubkey, pkey) = rsa.newkeys(2048, poolsize=4)
     open(WORKDIR+'private_server.pem', 'wb').write(pkey.save_pkcs1(format='PEM'))
     open(WORKDIR+'public_server.pem', 'wb').write(pubkey.save_pkcs1(format='PEM'))
     print('Keys saved in '+WORKDIR)
else:
     pkey = rsa.PrivateKey.load_pkcs1(pkeyfile)
     print('Server private key loaded')

@app.route('/domain', methods = ['POST'])
def check_domain():
     data = request.json
     try:
          message = rsa.decrypt(binascii.a2b_base64(data['message'].encode('utf8')), pkey)
          payload = json.loads(message.decode('utf8'))
     except rsa.pkcs1.DecryptionError as e:
          response = app.response_class(status=400)
          return response
     except binascii.Error:
         response = app.response_class(status=400)
         return response
     except TypeError:
         response = app.response_class(status=400)
         return response
     else:
          print('im in')
          domain = payload['domain']
          subdomains = payload['subdomains']
          signature = binascii.a2b_base64(data['signature'])
          pubkey = rsa.PublicKey.load_pkcs1(open(WORKDIR+'rsa/'+domain, 'r').read())
          ip = request.remote_addr
          try:
               verify = rsa.verify(message, signature, pubkey)
          except rsa.pkcs1.VerificationError:
               response = app.response_class(status=400)
               return response
          else:
               if verify:
                    print('in verify')
                    zone = easyzone.zone_from_file(domain, ZONEDIR+domain+'.db')
                    names = zone.get_names()
                    zone_change = False
                    for dom in subdomains:
                         print(dom+domain+'.')
                         print(names)
                         if dom == '':
                              subdom = domain + '.'
                         else:
                              subdom = dom + '.' + domain + '.'
                         try:
                              print(names[subdom])
                              this = names[subdom]
                         except KeyError:
                              pass
                         else:
                              if this.records('A').items[0] != ip:
                                   this.records('A').delete(this.records('A').items[0])
                                   this.records('A').add(ip)
                                   zone_change = True
                    if zone_change is True:
                         zone.save()
                         r = ZoneReload(rndc='/usr/sbin/rndc')
                         r.reload(domain)
                         print('Reload')
                    response = app.response_class(
                         status = 200
                    )
                    print('pre return')
                    return response

if __name__ == '__main__':
     app.debug = True
     app.run()
