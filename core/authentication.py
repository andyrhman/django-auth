import jwt, datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .models import User

class JWTAuthentication(BaseAuthentication):
    # * Alternative
    # ? https://chat.openai.com/c/de7103d9-24aa-428c-86e7-7914a8d0c86b
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            
            if not id:
                raise AuthenticationFailed('Unauthenticated')  # Properly handle unauthenticated case
            
            try:
                user = User.objects.get(pk=id)
                return (user, None) 
            except User.DoesNotExist:
                raise NotFound('User not found') 
        
        raise AuthenticationFailed('Unauthenticated')

def create_access_token(id):
    return jwt.encode({
        'user_id': str(id),  # Convert UUID to string
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=30),
        'iat': datetime.datetime.now(datetime.UTC)
    }, 'access_secret', algorithm='HS256')
    
def create_refresh_token(id, remember_me=False):
    if remember_me:
        exp_duration = datetime.timedelta(days=365)
    else:
        exp_duration = datetime.timedelta(seconds=30)
    expiration = datetime.datetime.now(datetime.timezone.utc) + exp_duration
    token = jwt.encode({
        'user_id': str(id),
        'exp': expiration,
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }, 'refresh_secret', algorithm='HS256')
    return token, expiration
    
def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        
        return payload['user_id']
    except Exception as e:
        print(e)
        return None

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')
        
        return payload['user_id']
    except Exception as e:
        print(e)
        return None