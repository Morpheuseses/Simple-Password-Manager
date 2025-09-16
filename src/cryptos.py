from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import filemanaging as fm
import pyclip
import os
from utils import hash_service
import base64

def get_privkey() -> str | None:
    path_ssh = fm.get_home() + "/" + ".ssh/id_ed25519"
    if os.path.exists(path_ssh):
            with open(path_ssh,"r") as f:
                privkey_data = f.read().strip().splitlines()
                b64 = "".join(line for line in privkey_data if not line.startswith("-----"))
            # print ("The key has been acquired")
            return b64
    else:
        return None
def init_pass(password: str, encoding:str = "utf-8"):
    pk = get_privkey()
    if pk is None:
        print ("You must do an ssh-keygen to get this work(id_ed25519 especially)")
        return
    print ("The key has been acquired")
    print ("Encryption of master...")
    salt = get_random_bytes(16)
    # use file with random number encoded into base64
    key = _derived_key(pk,salt)
    cipher = AES.new(key,AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode(encoding))
    blob = salt+nonce+tag+ciphertext
    fm.write_blob("master",blob)
    print ("Ecryption completed!")
def get_master(password: str, encoding: str = "utf-8") -> bytes | None:
    pk = get_privkey()
    if pk is None:
        print ("You must do an ssh-keygen to get this work(id_ed25519 especially)")
        return
    blob = fm.read_blob("master")
    s, n, t, ct = unpack_blob(blob)
    key = _derived_key(pk,s)
    cipher = AES.new(key,AES.MODE_EAX, nonce=n)
    try:
        master = cipher.decrypt_and_verify(ct,t)
        if password != master.decode(encoding):
            print("Master is incorrect")
            return None
    except:
        print ("Key is incorrect, try again")
        return None
    print ("Master is correct")
    return master
def _derived_key(password: str, salt:bytes, count=1200000):
   return PBKDF2(password,salt,32,count=count,hmac_hash_module=SHA512)
def unpack_blob(blob):
    # blob_bytes = blob.encode(encoding)
    salt       = blob[:16]
    nonce      = blob[16:32]
    tag        = blob[32:48]
    ciphertext = blob[48:]
    return salt, nonce, tag, ciphertext
def add_service(master: str, serv_name: str, serv_pass: str, encoding: str ="utf-8"):
    if not os.path.exists(fm.get_home() + "/" + fm.STORE_PATH + "/" + "master"):
        print ("First init master pass")
        return
    salt = get_random_bytes(16)
    key    = _derived_key(master,salt)
    cipher = AES.new(key,AES.MODE_EAX)
    nonce  = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(serv_pass.encode(encoding))
    blob_bytes = salt+nonce+tag+ciphertext
    blob = base64.b64encode(blob_bytes).decode(encoding)
    fm.add_serviceJSON(serv_name,blob)
def delete_service(master: str, serv_name: str):
    if decrypt_and_verify(master, serv_name):
        fm.delete_serviceJSON(serv_name)
def decrypt_and_verify(password: str, serv_name: str) -> bool:
    if os.path.exists(fm.get_home() + "/" + fm.STORE_PATH + "/" + "pass.json"):
        data = fm.readJSON("pass.json")
    else:
        print ("There is no pass.json initialized")
        return False
    if len(data) == 0:
        print("There is no services in the database")
        return False
    blob = base64.b64decode(data[hash_service(serv_name)])
    s, n, t, ct = unpack_blob(blob)
    key = _derived_key(password,s)
    cipher = AES.new(key,AES.MODE_EAX,nonce=n)
    try:
        cipher.decrypt_and_verify(ct, t)
    except:
        return False
    return True
def decrypt_and_CopyAES(password: str, serv_name: str, encoding: str ="utf-8"):
    if os.path.exists(fm.get_home() + "/" + fm.STORE_PATH + "/" + "pass.json"):
        data = fm.readJSON("pass.json")
    else:
        print ("There is no pass.json initialized")
        return
    if len(data) == 0:
        print("There is no services in the database")
        return
    blob = base64.b64decode(data[hash_service(serv_name)])
    s, n, t, ct = unpack_blob(blob)
    key = _derived_key(password,s)
    cipher = AES.new(key,AES.MODE_EAX,nonce=n)
    try:
        plaintext = cipher.decrypt_and_verify(ct, t)
        print ("Master is valid")
        pyclip.copy(plaintext.decode(encoding))
        print ("Here your password service called(in your clipboard): ",serv_name)
    except:
        print ("Blob or Master is invalid")
        return False
    return True
