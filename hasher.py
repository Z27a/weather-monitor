import hashlib
pword = 'email@email.com'
pword = (hashlib.sha256(pword.encode('utf-8'))).hexdigest()

print(pword)