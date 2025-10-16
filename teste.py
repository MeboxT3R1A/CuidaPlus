import hashlib


a = input("Digite algo: ")
print(hashlib.sha256(a.encode()).hexdigest())
