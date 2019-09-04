import subprocess
import os
import rsa

PATH = '/opt/dyndns'


def create_venv(interpreter, path):
    res = subprocess.check_call('virtualenv -p {} {}'.format(interpreter, path), shell=True)
    if res == 0:
        return True
    else:
        return False


def install_python_requirements(path):
    res = subprocess.check_call('{}/bin/pip install dnspython'.format(path), shell=True)
    if res == 0:
        res = subprocess.check_call('{}/bin/pip install -r {}/requirements.txt'.format(path, path), shell=True)
        if res == 0:
            libdirs = os.listdir(path+'/lib/')
            for dir in libdirs:
                if 'python' in dir:
                    pyv = dir
                else:
                    return False
            res = subprocess.check_call('mv {}/easyzone.py {}/lib/{}/site-packages/easyzone/'.format(path,
                                                                                                     path,
                                                                                                     pyv), shell=True)
            if res == 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def add_user(path):
    res = subprocess.check_call('useradd -s /bin/false -G bind -d {} dyndns'.format(path), shell=True)
    if res == 0:
        return True
    else:
        return False


def dirop(path):
    res = subprocess.check_call('mkdir -p {}/rsa {}/client/rsa'.format(path, path), shell=True)
    if res == 0:
        res = subprocess.check_call('chown -Rc dyndns:bind {}'.format(path), shell=True)
        if res == 0:
            return True
        else:
            return False
    else:
        return False


def create_service(path):
    res = subprocess.check_call('mv {}/dyndns.service /etc/systemd/system/'.format(path), shell=True)
    if res == 0:
        return True
    else:
        return False

def gen_newkeys():
    print('Generation new RSA keys...')
    (pubkey, pkey) = rsa.newkeys(2048, poolsize=4)
    open(WORKDIR + 'private_server.pem', 'wb').write(pkey.save_pkcs1(format='PEM'))
    open(WORKDIR + 'public_server.pem', 'wb').write(pubkey.save_pkcs1(format='PEM'))
    print('Done')


create_venv('/usr/bin/python3', PATH)
install_python_requirements(PATH)
add_user(PATH)
create_service(PATH)
dirop(PATH)
gen_newkeys()
