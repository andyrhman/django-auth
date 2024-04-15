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
                return (user, None)  # Correctly return user and auth
            except User.DoesNotExist:
                raise NotFound('User not found')  # Raise NotFound instead of returning Response
        
        raise AuthenticationFailed('Unauthenticated')  # Raise exception if no auth provided

def create_access_token(id):
    return jwt.encode({
        'user_id': str(id),  # Convert UUID to string
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=30),
        'iat': datetime.datetime.now(datetime.UTC)
    }, 'access_secret', algorithm='HS256')
    
def create_refresh_token(id, remember_me=False):
    if remember_me:
        # Set expiration to 1 year if "remember me" is checked
        exp_duration = datetime.timedelta(days=365)
    else:
        # Set expiration to 30 seconds if "remember me" is not checked
        exp_duration = datetime.timedelta(seconds=30)
    return jwt.encode({
        'user_id': str(id),  # Convert UUID to string
        'exp': datetime.datetime.now(datetime.UTC) + exp_duration,
        'iat': datetime.datetime.now(datetime.UTC)
    }, 'refresh_secret', algorithm='HS256')
    
def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        
        return payload['user_id']
    except Exception as e:
        print(e)
        return None