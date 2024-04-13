import jwt, datetime

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