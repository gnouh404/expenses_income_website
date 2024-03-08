from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

# protect route, tránh việc đã log out ấn quay lại vẫn ở tài khoản chưa đăng xuất
@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    context ={
        'expenses':expenses,
        'categories':categories,
    }
    return render(request, 'expenses/index.html',context)

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