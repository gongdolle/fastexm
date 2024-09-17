from fastapi import APIRouter,Depends,HTTPException
from src.schema.request import SignUpRequest ,LogInRequest
from src.service.user import UserService
from src.database.orm import User
from src.database.repository import UserRepository
from src.schema.respones import UserSchema ,JWTResponse
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