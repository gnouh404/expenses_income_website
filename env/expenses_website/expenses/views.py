from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
#  for divide page
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
# Create your views here.

# protect route, tránh việc đã log out ấn quay lại vẫn ở tài khoản chưa đăng xuất
@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    # arg 1 la noi dung muon phan chia, arg 2 la so noi dung phan chia trong 1 trang
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user = request.user).currency
    context ={
        'expenses':expenses,
        'categories':categories,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request, 'expenses/index.html',context)

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchTxt')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner = request.user) | Expense.objects.filter(
            description__icontains=search_str, owner = request.user) | Expense.objects.filter(
            category__icontains=search_str, owner = request.user) | Expense.objects.filter(
            date__icontains=search_str, owner = request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)    

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
        'values':request.POST
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expense.html', context)
    # kiem soat dau vao cua ng dung
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)  
        Expense.objects.create(amount = amount, description = description, owner = request.user, date = date, category = category)
        messages.success(request, 'Add expense successfully')
        return redirect('expenses')
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method == "GET":
        return render(request, 'expenses/edit-expense.html',context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit-expense.html', context)  
        expense.amount = amount 
        expense.description = description  
        expense.date = date 
        expense.category = category
        expense.save()
        messages.success(request, 'Edit expense successfully')
        return redirect('expenses')
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()      
    messages.success(request, "Expense removed")
    return redirect('expenses')     