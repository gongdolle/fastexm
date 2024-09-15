import bcrypt


password="password"

byte_passward=password.encode("UTF-8")

hash_1=bcrypt.hashpw(byte_passward,salt=bcrypt.gensalt())
hash_2=bcrypt.hashpw(byte_passward,salt=bcrypt.gensalt())

print(hash_1)
print(hash_2)

print(bcrypt.checkpw(byte_passward,hash_1))
print(bcrypt.checkpw(byte_passward,hash_2))



