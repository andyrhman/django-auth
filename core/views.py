from datetime import datetime, timedelta, timezone
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import exceptions
from .models import User, UserToken
from .authentication import JWTAuthentication, create_access_token, create_refresh_token, decode_refresh_token

class RegisterAPIView(APIView):
    def post(self, request):
        try:  
            data = request.data
            
            if 'password' not in data or 'password_confirm' not in data:
                return Response({"message": "Both password and password confirmation are required"}, status=status.HTTP_400_BAD_REQUEST)

            if data['password'] != data['password_confirm']:
                return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSerializer(data=data)

            # * Validation check
            try:
                serializer.is_valid(raise_exception=True)
            except exceptions.ValidationError as e:
                # Generate a more user-friendly message that includes the field name
                errors = {key: value[0] for key, value in e.detail.items()}  # Create a dictionary of field: first_error
                first_field = next(iter(errors))  # Get the first field with an error
                field_name = first_field.replace('_', ' ').capitalize()  # Make field name more readable
                # Customize error messages for common cases
                if 'required' in errors[first_field]:
                    message = f"{field_name} is required."
                elif 'already exists' in errors[first_field]:
                    message = f"{field_name.lower()} already exists."
                else:
                    message = f"{field_name} error: {errors[first_field]}"
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if config('DEBUG', cast=bool):
                print(e)
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        try:  
            data = request.data
            
            if 'email' not in data:
                return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' not in data:
                return Response({"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data['email']
            password = request.data['password']
            remember_me = data.get('rememberMe', False)  # Default to False if not provided
            
            user = User.objects.filter(email=email).first()
            
            if user is None:
                return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.check_password(password):
                return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id, remember_me)
            
            UserToken.objects.create(
                user_id=user.id,
                token=refresh_token,
                expired_at=datetime.now(timezone.utc) + timedelta(days=7)
            )
            
            response = Response()
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            response.data = {
                'token': access_token
            }
            
            return response
        except Exception as e:
            if config('DEBUG', cast=bool):
                print(e)
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:   
            # * Alternative
            # ? https://chat.openai.com/c/de7103d9-24aa-428c-86e7-7914a8d0c86b
            return Response(UserSerializer(request.user).data)
        except Exception as e:
            if config('DEBUG', cast=bool):
                print(e)
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
class RefreshAPIView(APIView):
    def post(self, request):
        try:       
            refresh_token = request.COOKIES.get('refresh_token')
            
            if not refresh_token:
                return Response({'message': 'Unauthenticated'}, status=status.HTTP_403_FORBIDDEN)

            id = decode_refresh_token(refresh_token)
            
            if not id:
                return Response({'message': 'Unauthenticated'}, status=status.HTTP_403_FORBIDDEN)
            
            if not UserToken.objects.filter(
                user_id=id,
                token=refresh_token,
                expired_at__gt=datetime.now(timezone.utc)
            ).exists():
                return Response({"message": "Unauthenticated"}, status=status.HTTP_403_FORBIDDEN)
            
            access_token = create_access_token(id)
            
            return Response({"token": access_token})
        except Exception as e:
            if config('DEBUG', cast=bool):
                print(e)
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
            
class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:    
            UserToken.objects.filter(user_id=request.user.id).delete()
            
            response = Response()
            response.delete_cookie(key='refresh_token')
            response.data = {
                "message": "success"
            }
            
            return response
        except Exception as e:
            if config('DEBUG', cast=bool):
                print(e)
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        