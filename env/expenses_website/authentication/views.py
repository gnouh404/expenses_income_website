
from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
# Create your views here.
# validate_email chua dung
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email ko hop le'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email đã tồn tại'}, status=409)
        return JsonResponse({'email_valid':True})  


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username chỉ chứa chữ và số'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username đã tồn tại'}, status=409)
        return JsonResponse({'username_valid':True})    
            
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        # cac kieu thong bao khi nhan register
        
        # messages.warning(request, 'Success warning')
        # messages.info(request, 'Success info')
        # messages.error(request, 'Success error')
        
        messages.success(request, 'Success')
        return render(request, 'authentication/register.html')
        
        