from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/login')


# no using this just for knowing how it works, i wrote this part
# class TokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         auth_credentials = await super().__call__(request)
        
#         token = auth_credentials.credentials
        
#         if token is None:
#             raise NotAuthenticatedException()
        
#         return token
    
    
# access_token_bearer = TokenBearer()

# token_bearer = Annotated[dict, Depends(access_token_bearer)]