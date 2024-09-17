import bcrypt


class UserService:
    encoding:str="UTF-8"
    secret_key: str="4c8fb0aa1036155371100650650aef3758485bdf33ef60b9b233543cc2d472b9"
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
        
    def create_jwt(self,payload:dict)->str:
        return 
        
    