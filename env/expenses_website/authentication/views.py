
from django.shortcuts import render,redirect,HttpResponse
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
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

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
            "values":request.POST
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
                # lấy miền của người dùng đang sử dụng, url tương đối, mã hóa id user, tạo token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token': account_activation_token.make_token(user)})
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
                #  cho phép các hoạt động trong phương thức run() chạy song song với các hoạt động khác trong ứng dụng của bạn, giúp tăng hiệu suất và khả năng xử lý đa luồng
                EmailThread(email).start()
                messages.success(request, "Account successfully created")
                return render(request, 'authentication/register.html')
            
        return render(request, 'authentication/register.html')

# giải mã uid, token        
class VerificationView(View):
    def get(self, request, uidb64, token):
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            # check nếu link người dùng ấn vào từ gmail đã active(check user và token có từ link) thì sẽ trả về trang login và thông báo
            if not account_activation_token.check_token(user, token):
                messages.info(request, 'User already activated')
                return redirect('login')
            # nếu user đã active thì về login, ko thì set active = true, lưu và trả về thông báo
            if user.is_active:
                return redirect('login')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                return redirect('login')
        
        except Exception as ex:
            pass        
        
        return redirect('login')
           
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')      
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # Nếu điền đủ username và pass
        if username and password:
            user = auth.authenticate(username=username, password=password)
            # auth.authenticate trả về user object, check xem có phải user tồn tại ko. Tồn tại thì kiểm tra active, chưa active thì đưa ra tn ktra mail
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('expenses')
                messages.error(request, 'Your account is not activated, please check your email')
                return render(request, 'authentication/login.html')
            # user is None nghĩa là user ko tồn tại hoặc sai mk, username
            else:
                messages.error(request, 'Invalid credential, try again')
                return render(request, 'authentication/login.html')
        # Điền ko đủ username và pass sẽ bắt điền lại    
        else:
            messages.error(request, 'Fill all the fields')
            return render(request, 'authentication/login.html')    
        
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have logged out successfully')
        return redirect('login')
    
class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    def post(self, request):
        email = request.POST['email']
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Email is not valid')
            return render(request, 'authentication/reset-password.html', context=context)
        
        user = User.objects.filter(email=email)
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            
            
            email_contents={
                'domain':domain,
                'user':user[0],
                'uidb64':uidb64,
                'token':PasswordResetTokenGenerator().make_token(user[0]),
            }
            link = reverse('reset-user-password', kwargs={'uidb64':email_contents['uidb64'], 'token': email_contents['token']})
            # gửi mail để xác nhận
            email_subject = "Activate your account"
            reset_url = "http://" + domain + link
            email_body = "Hi " + user[0].username + " Please use this link to reset your password\n" + reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@example.com",
                [email],
            )
            #  cho phép các hoạt động trong phương thức run() chạy song song với các hoạt động khác trong ứng dụng của bạn, giúp tăng hiệu suất và khả năng xử lý đa luồng
            EmailThread(email).start()
            messages.success(request, 'Please check your email!')
            return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            # check if the link is used before
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'The link is used before, request a new one')
                return render(request, 'authentication/reset-password.html')
        except Exception:
            pass
        return render(request, 'authentication/set-new-password.html', context)
    def post(self, request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        if password2 != password:
            messages.error(request, 'Password is not match')
            return render(request, 'authentication/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, 'Password too short!')
            return render(request, 'authentication/set-new-password.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        except Exception:
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'authentication/set-new-password.html', context)
# speed up email sending
class EmailThread(threading.Thread):
    def __init__(self, email) :
        self.email = email
        threading.Thread.__init__(self)
    def run(self) :
        self.email.send(fail_silently=False)       
                    