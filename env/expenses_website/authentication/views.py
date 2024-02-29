
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
        # messages.success(request, 'Success')
        # return render(request, 'authentication/register.html')
        # get user data
        # validate
        # create user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # thêm đối số context vào khi ko đúng định dạng mật khẩu sẽ giữ nguyên username và email
        context ={
            "fieldVal":request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password is too short")
                    return render(request, 'authentication/register.html',context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Account successfully created")
                return render(request, 'authentication/register.html')
            
        return render(request, 'authentication/register.html')
        
        
        
        