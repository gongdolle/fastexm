from fastapi import APIRouter
from src.schema.request import SignUpRequest
router=APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201)
def user_sign_up_handler(request:SignUpRequest):
    #1.request body(username,password)
    #2.password->hashing->hashed_password
    #3. user(username,hashed_password)
    #4. user->db save
    #5. return user(id)
    
    
    return True