from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from src.schema.request import SignUpRequest ,LogInRequest ,CreateOTPRequset,VerifyOTPRequest
from src.service.user import UserService
from src.database.orm import User
from src.database.repository import UserRepository
from src.schema.respones import UserSchema ,JWTResponse
from src.security import get_access_token
from src.cache import redis_client
router=APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201)
def user_sign_up_handler(
    request:SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository =Depends(),
    ):
    #1.request body(username,password)
    #2.password->hashing->hashed_password
    hashed_password :str =user_service.hash_password(
        plain_password=request.password
    )
    #3. user(username,hashed_password)
    user:User=User.create(
        username=request.username,
        hashed_password=hashed_password
    )
    
    
    #4. user->db save
    user:User=user_repo.save_user(user=user) #id=int
    
    
    #5. return user(id)
    
    
    return UserSchema.from_orm(user)

@router.post("/log-in")
def user_log_in_handler(
    request: LogInRequest,
    user_repo:UserRepository=Depends(),
    user_service: UserService=Depends(),
    
):
    #1.request body(username, password)
    
    
    #2.db read user
    user:User| None =user_repo.get_use_by_username(
        username=request.username
    )
    
    
    if not user:
        raise HTTPException(status_code=404,detail= "User Not Found")
    
    
    
    #3. user.password ,request.password-> bcrpyt.checkpw
    verified:bool=user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    
    )
    
    if not verified:
        raise HTTPException(status_code=401,detail="Not Authorized")
    
    #4. create jwt
    access_token:str= user_service.create_jwt(username=user.username)
    #5. reuturn jwt
    return JWTResponse(access_token=access_token)



#회원가입은 (username,password)/로그인
# 이메일 추가인증후 알림
#post /user/email/otp -> email key ,value: otp code exp:3
#post /user/email/verify -> request(email, otp)->user(email)



@router.post("/email/otp")
def create_otp_handler(
    request:CreateOTPRequset,
    _:str=Depends(get_access_token),
    user_service: UserService=Depends(),
):
    #1. access_token
    #2. request body(email)
    #3. otp create(random 4 digit)
    otp:int =user_service.create_otp()
    
    #4. redis otp(email , ort exp=3min)
    redis_client.set(request.email,otp)
    redis_client.expire(request.email,3*60)
    #5. send otp to email
    
    return {"otp":otp}

@router.post("/email/otp/verify")
def verify_otp_handler(
    request:VerifyOTPRequest,
    backgroud_tasks:BackgroundTasks,
    access_token:str=Depends(get_access_token),
    user_service: UserService=Depends(),
    user_repo: UserRepository=Depends(),
):
    #1.access_token
    #2.request body
    otp:str|None =redis_client.get(request.email)
    if not otp:
        raise HTTPException(status_code=400,detail="Bad Requset")
    if request.otp !=int( otp):
        raise HTTPException(status_code=400,detail="Bad Request")
    #3.requset .otp==redis.get(email)
    username:str= user_service.decode_jwt(access_token=access_token)
    user:User | None = user_repo.get_use_by_username(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    #save email to user
    
    #4. user(email)
    backgroud_tasks.add_task(
        user_service.send_email_to_user,
        email="admin@fastapi.com"
    )
   
    return UserSchema.from_orm(user)

