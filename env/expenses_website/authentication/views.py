
from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
# url tương đối tới verification
# mã hóa uid, token
from django.urls import reverse   
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
# Create your views here.
# validate_email chua dung
# View là class có sẵn của django dùng làm lớp cha của các lớp cần tạo
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
                user.is_active = False
                user.save()
                # lấy miền của người dùng đang sử dụng, url tương đối
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token': token_generator.make_token(user)})
                active_url = "http://" + domain + link
                # gửi mail để xác nhận
                email_subject = "Activate your account"
                email_body = "Hi " + user.username + " Please use this link to verify your account\n" + active_url
                
                
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@example.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account successfully created")
                return render(request, 'authentication/register.html')
            
        return render(request, 'authentication/register.html')
# url tương đối tới verification
# mã hóa uid, token        
class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')
            
        
        