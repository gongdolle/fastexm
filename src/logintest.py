import bcrypt


password="password"

byte_passward=password.encode("UTF-8")
hash_1=bcrypt.hashpw(byte_passward,salt=bcrypt.gensalt())
hash_1=hash_1.decode("UTF-8")
print(hash_1)
