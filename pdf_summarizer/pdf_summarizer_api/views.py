from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import PDfDocumentSerializer, UserLoginSerializer, UserRegisterSerializer
from .models import PDFDocument, User
from .forms import SignUpForm
from .chat_functions import set_open_params, get_completion
import requests
import PyPDF2


# Create your views here.

class GenerateSummary(APIView):
    
    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        
        if not pdf_file:
            return Response({'error':'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            num_pages = len(pdf_reader.pages)

            pdf_text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                pdf_text += text
           
            messages = [
                {
                    "role": "system",
                    "content":"You are expert pdf summarizer. You take pdf text from user as an input and provide a good summary as a output."
                },
                {
                    "role":"user",
                    "content":f"Provide summary for following text: {pdf_text}"
                }
            ]
            params = set_open_params()
            summary = get_completion(params=params, messages=messages)
            print(summary)
            
            pdf_document = PDFDocument.objects.create(
                title = 'pdf_file',
                uploaded_file = pdf_file,
                summary = summary,
                user_id = int(request.POST.get('user_id'))
            )
            serializer = PDfDocumentSerializer(pdf_document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'{e}'}, status = status.HTTP_400_BAD_REQUEST)
      

def signup(request):
    if request.method == 'POST':
        # drf_request = Request(request)
        # form_data = drf_request.data
        data = request
        response = requests.post(f"{settings.API_BASE_URL}/api/sign-up/", data=data)

        if response.status_code == 201:
            messages.success(request, 'sign up successful! Please L')
            return redirect('signup.html')
        else:
            messages.error(request, "Sign Up failed. Try Again")
            return redirect('signup.html')
    else:
        return render(request, 'signup.html', {'form': SignUpForm})


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    #   authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        print(request.user.id)
        token = Token.objects.get(user_id=request.user.id)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)