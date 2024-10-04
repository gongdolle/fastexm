import random
import bcrypt
import time
from datetime import datetime ,timedelta
from jose import jwt

class UserService:
    encoding:str="UTF-8"
    #openssl rand -hex 32
    secret_key: str="4c8fb0aa1036155371100650650aef3758485bdf33ef60b9b233543cc2d472b9"
    
    jwt_algorithm:str="HS256"
    
    def hash_password(self, plain_password:str)->str:
        hashed_password:bytes=bcrypt.hashpw(
            plain_password.encode(self.encoding),salt=bcrypt.gensalt()
            )
        return hashed_password.decode(self.encoding)
    
    def verify_password(
        self,
        plain_password:str , 
        hashed_password:str
        )-> bool:
        #try/except 나중에추가
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
            )
        
    def create_jwt(self,username:str)->str:
        return jwt.encode(
            {   
              #uniqe id
              "sub": username,
              #On expiration
              "exp": datetime.now()+timedelta(days=1),
             },
            self.secret_key,
            algorithm=self.jwt_algorithm,
            )
        
    def decode_jwt(self,access_token:str)->str:
        payload:dict= jwt.decode(
            access_token,self.secret_key,algorithms=[self.jwt_algorithm]
        )        
        
        return payload["sub"]
    
    @staticmethod
    def create_otp()->int:
        return random.randint(1000,9999)
    @staticmethod
    def send_email_to_user(email:str)-> None: 
        time.sleep(10)
        print(f"send email to {email}")
        