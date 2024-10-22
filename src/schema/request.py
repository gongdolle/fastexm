from pydantic import BaseModel,EmailStr

class IdcheckRequset(BaseModel):
    username:str


class CreateToDoRequest(BaseModel):
    contents:str
    is_done : bool
    
class SignUpRequest(BaseModel):
    username: str
    name: str
    phone_num: str
    email: EmailStr
    com_num: str
    password: str
  

   
    
class LogInRequest(BaseModel):
    username : str
    password : str


class CreateOTPRequset(BaseModel):
    email:str
    
class VerifyOTPRequest(BaseModel):
    email:str
    otp:int
    