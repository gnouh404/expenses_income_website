from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
#  for divide page
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner = request.user)
    # arg 1 la noi dung muon phan chia, arg 2 la so noi dung phan chia trong 1 trang
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user = request.user).currency
    context ={
        'income':income,
        'sources':sources,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request, 'income/index.html',context)

@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources':sources,
        'values':request.POST
    }
    if request.method == "GET":
        return render(request, 'income/add_income.html', context)
    # kiem soat dau vao cua ng dung
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)  
        Income.objects.create(amount = amount, description = description, owner = request.user, date = date, source = source)
        messages.success(request, 'Add income successfully')
        return redirect('income')
    
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchTxt')
        income = Income.objects.filter(
            amount__icontains=search_str, owner = request.user) | Income.objects.filter(
            description__icontains=search_str, owner = request.user) | Income.objects.filter(
            source__icontains=search_str, owner = request.user) | Income.objects.filter(
            date__icontains=search_str, owner = request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False) 

def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context={
        'income':income,
        'values':income,
        'sources':sources
    }
    if request.method == "GET":
        return render(request, 'income/edit-income.html',context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit-income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit-income.html', context)  
        income.amount = amount 
        income.description = description  
        income.date = date 
        income.source = source
        income.save()
        messages.success(request, 'Edit income successfully')
        return redirect('income')
    
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()      
    messages.success(request, "Income removed")
    return redirect('income')

def income_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=30*6)
    incomes = Income.objects.filter(owner = request.user,date__gte = six_months_ago, date__lte = today_date).order_by("source")
    finalrep = {}
    
    def get_category(income):
        return income.source
    
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source = source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    # set remove duplicate
    source_list = list(set(map(get_category, incomes)))
    
    for x in incomes:
        for y in source_list:
            # set key     set value
            finalrep[y] = get_income_source_amount(y)
    sorted_dict = {k: v for k, v in sorted(finalrep.items(), key=lambda item: item[1])}
    return JsonResponse({'income_source_data':sorted_dict}, safe=False)

def income_stats_view(request):
    return render(request, 'income/income-stats.html')         