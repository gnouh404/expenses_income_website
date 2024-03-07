from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.
def index(request):
    # tạo 1 list rỗng để lưu dictionary của các loại tiền tệ
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k,'value':v})
    # 1 biến để ktra user có tồn tại ko         
    exists = UserPreference.objects.filter(user=request.user).exists()
    # đặt đối tượng tiền tệ của user là none
    user_preferences = None
    # Nếu tồn tại user thì gán đối tượng user_preferences cho user hiện tại
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    # Trả về phía ng dùng file index, bao gồm dữ liệu currencies là các loại tiền tệ để ng dùng chọn, user_preferences của người dùng    
    if request.method == "GET":
        return render(request, 'preferences/index.html',{'currencies':currency_data, 'user_preferences':user_preferences})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:   
            UserPreference.objects.create(user=request.user, currency = currency)    
        messages.success(request, "Changes saved")
        return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences})
         