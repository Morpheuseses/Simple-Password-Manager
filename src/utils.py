import hashlib

def hash_service(name: str, encoding: str ="utf-8") -> str:
   return hashlib.sha256(name.encode(encoding)).hexdigest()
