from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from django.conf import settings
from .models import Student
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import LogoutSerializer
import urllib.parse
import traceback
 
from .serializers import StudentRegistrationSerializer as RegisterSerializer, StudentLoginSerializer as LoginSerializer, StudentProfileSerializer as StudentSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print("serializer:", serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            # Convert token to string explicitly
            token = str(RefreshToken.for_user(user).access_token)
            
            # Update verification URL to match the backend endpoint
            verification_url = f"http://localhost:8000/api/students/verify-email/{token}/"

            # Create HTML email with button
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                    .container {{ padding: 20px; }}
                    h1 {{ color: #00AA44; }}
                    .button {{ background-color: #00FF40; color: #000; padding: 12px 24px; text-decoration: none; 
                              display: inline-block; border-radius: 50px; font-weight: bold; margin: 20px 0; }}
                    .button:hover {{ background-color: #00DD30; }}
                    .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to GyanSort!</h1>
                    <p>Hello {user.fullname},</p>
                    <p>Thank you for registering with GyanSort. Please verify your email address to complete your registration.</p>
                    <p><a href="{verification_url}" class="button">Verify Email Address</a></p>
                  
                    <p>This link will expire in 60 minutes.</p>
                    <p>If you did not register for GyanSort, please ignore this email.</p>
                    <div class="footer">
                        <p>Best regards,<br>The GyanSort Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version for email clients that don't support HTML
            text_content = f"""
            Welcome to GyanSort!
            
            Hello {user.fullname},
            
            Thank you for registering with GyanSort. Please verify your email address to complete your registration.
            
            Verification link: {verification_url}
            
            This link will expire in 60 minutes.
            
            If you did not register for GyanSort, please ignore this email.
            
            Best regards,
            The GyanSort Team
            """
            
            # Create email message with both HTML and plain text
            subject = "Verify Your GyanSort Account"
            from_email = settings.EMAIL_HOST_USER
            to = [user.email]
            
            # Create the email message
            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, "text/html")
            
            # Send the email
            email.send()
            
            return Response({"message": "User registered. Check email for verification"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            print(f"Received verification request with token: {token}")
            
            # Handle potential URL encoding issues
            token = urllib.parse.unquote(token)
            
            try:
                # Decode the token
                token_obj = AccessToken(token)
                user_id = token_obj['user_id']  # Access user_id directly
                print(f"Decoded user_id: {user_id}")
                
                user = Student.objects.get(id=user_id)
                print(f"Found user: {user.email}")
                
                if user.email_verified:
                    print("User already verified")
                    return Response({
                        'success': True,
                        'message': 'Email already verified',
                        'redirect': '/login'
                    }, status=status.HTTP_200_OK)
                
                # Update user verification status
                user.is_active = True
                user.email_verified = True
                user.save()
                print(f"User {user.email} verified successfully")
                
                return Response({
                    'success': True,
                    'message': 'Email verified successfully',
                    'redirect': '/login'
                }, status=status.HTTP_200_OK)
                
            except TokenError as e:
                print(f"Token error: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'Invalid or expired verification token'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                print("User not found")
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'success': False,
                'message': 'Verification failed. Please try again or contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])
            if user:
                if not user.is_active:
                    return Response({"error": "Account is not active"}, status=status.HTTP_403_FORBIDDEN)
                if not user.email_verified:
                    return Response({"error": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)
                token = RefreshToken.for_user(user)
                return Response({
                    "access": str(token.access_token), 
                    "refresh": str(token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "fullname": user.fullname,
                        "student_id": user.student_id,
                        "verification_status": user.verification_status
                    }
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = StudentSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = StudentSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Then your LogoutView class should work correctly
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)