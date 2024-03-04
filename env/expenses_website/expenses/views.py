from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# protect route, tránh việc đã log out ấn quay lại vẫn ở tài khoản chưa đăng xuất
@login_required(login_url="/authentication/login")
def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')
