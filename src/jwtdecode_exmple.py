from jose import jwt



access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcyNjcxNTQyMH0.GUXSyVNg-ahM-5urKcfffNO9N5_Bf4j2M27AiFHSfNg"
secret_key: str="4c8fb0aa1036155371100650650aef3758485bdf33ef60b9b233543cc2d472b9"
jwt_algorithm:str="HS256"

a=jwt.decode(access_token,secret_key,algorithms=[jwt_algorithm])
print(a)