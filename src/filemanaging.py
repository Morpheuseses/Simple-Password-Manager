import json
import os
from utils import hash_service
import base64

STORE_PATH = ".spm"

def check_master() -> bool:
    return os.path.exists(get_home() + "/" + STORE_PATH + "/" + "master")
def get_home() -> str:
    home: str = os.path.expanduser("~")
    if home == "":
        raise Exception("There is no users $HOME")
    return home
def write_blob(desc: str, data:bytes, encoding: str ="utf-8"):
    home: str = get_home()
    if not os.path.exists(home + "/" + STORE_PATH):
        os.makedirs(home + "/" + STORE_PATH)
    with open(home + "/"+ STORE_PATH + "/" +  desc,"w") as f:
        f.write(base64.b64encode(data).decode(encoding))
def read_blob(desc: str, encoding: str ="utf-8"):
    home: str = get_home()
    with open(home + "/" + STORE_PATH + "/" + desc,"r") as f:
        blob = f.read()
    return base64.b64decode(blob)
def add_serviceJSON(name: str, blob: str):
    if not os.path.exists( get_home() + "/" + STORE_PATH + "/" + "pass.json"):
        emp = {}
        with open("pass.json","w") as f:
            json.dump(emp,f)
        data = {}
    else:
        data = readJSON("pass.json")
    data[hash_service(name)] = blob
    writeJSON("pass.json",data)
    print("Service added",name)
def delete_serviceJSON(name: str):
    if not os.path.exists( get_home() + "/" + STORE_PATH + "/" + "pass.json"):
        return
    data = readJSON("pass.json")
    data.pop(hash_service(name),None)
    writeJSON("pass.json",data)
    print("Service deleted",name)
def writeJSON(desc: str, d: dict):
    path: str = get_home() + "/" + STORE_PATH + "/" + desc
    with open(path,"w") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)
def readJSON(desc: str) -> dict:
    path: str = get_home() + "/" + STORE_PATH + "/" + desc
    with open(path, "r") as f:
       data = json.load(f)
    return data
def save_master_salt_n_count(salt:bytes, count: int, encoding: str ="utf-8"):
    path: str = get_home() + "/" + STORE_PATH + "/" + "master"
    with open(path,"wb") as f:
        f.write(count.to_bytes(4,"big"))
        f.write(salt)
def load_master_salt_n_count():
    path: str = get_home() + "/" + STORE_PATH + "/" + "master"
    with open(path,"wb") as f:
        count = int.from_bytes(f.read(4),"big")
        salt = f.read()
    return salt, count
