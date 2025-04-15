from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from home.models import Farm, Income, Expenditure, Farm
from itertools import chain
from django.db.models import Sum
from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Farmer

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        address = request.POST['address']

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        farmer = Farmer.objects.create(user=user, phone=phone, address=address)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect superusers to admin interface
            if user.is_superuser:
                return redirect('admin:index')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    farmer = request.user.farmer
    total_budget = Farm.objects.filter(farmer=farmer).aggregate(total_budget=Sum('crop_budget'))['total_budget'] or 0
    total_income = Income.objects.filter(farm__farmer=farmer).aggregate(total_income=Sum('amount'))['total_income'] or 0
    total_expenditure = Expenditure.objects.filter(farm__farmer=farmer).aggregate(total_expenditure=Sum('amount'))['total_expenditure'] or 0

    # Data for graphs
    farms = Farm.objects.filter(farmer=farmer)
    crop_names = [farm.crop_name for farm in farms]
    crop_budgets = [farm.crop_budget for farm in farms]

    expenditures = Expenditure.objects.filter(farm__farmer=farmer)

    # Merge expenditures with the same details
    merged_expenditures = defaultdict(int)
    for expenditure in expenditures:
        merged_expenditures[expenditure.details] += expenditure.amount

    # Prepare data for the graph
    expenditure_details = list(merged_expenditures.keys())
    expenditure_amounts = list(merged_expenditures.values())

    context = {
        'total_budget': total_budget,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'crops': farms,  # Updated to use Farm objects
        'crop_names': crop_names,
        'crop_budgets': crop_budgets,
        'expenditure_details': expenditure_details,
        'expenditure_amounts': expenditure_amounts,
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def addFarm(request):
    context={'success': False}
    if request.method == 'POST':
        crop_name = request.POST['crop_name']
        farm_name = request.POST['farm_name']
        Description = request.POST['description']
        Budget = request.POST['budget']
        ins = Farm(
            crop_name=crop_name,
            farm_name=farm_name,
            crop_description=Description,
            crop_budget=Budget,
            farmer=request.user.farmer
        )
        ins.save()
        context={'success': True}
        print(crop_name, farm_name,Description, Budget)
    return render(request, 'addFarm.html', context)

@login_required(login_url='login')
def farms(request):
    all_farms = Farm.objects.filter(farmer=request.user.farmer)
    context = {'farms': all_farms}
    return render(request, 'farms.html', context)

@login_required(login_url='login')
def farm_detail(request, farm_id):
    # Fetch the Farm object with related Income and Expenditure objects
    farm = get_object_or_404(Farm.objects.prefetch_related('income_set', 'expenditure_set'), id=farm_id, farmer=request.user.farmer)
    
    # Calculate total income and expenditure using Django's aggregate function
    total_income = farm.income_set.aggregate(total=Sum('amount'))['total'] or 0
    total_expenditure = farm.expenditure_set.aggregate(total=Sum('amount'))['total'] or 0
    
    # Fetch all farms
    all_farms = Farm.objects.filter(farmer=request.user.farmer)
    
    context = {
        'farm': farm,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'incomes': farm.income_set.all(),
        'expenditures': farm.expenditure_set.all(),
        'all_farms': all_farms
    }
    return render(request, 'farm_detail.html', context)

@login_required(login_url='login')
def add_income_expenditure(request):
    if request.method == 'POST':
        farm_id = request.POST['farm_id']
        # Verify the farm belongs to the current farmer
        farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
        amount = int(request.POST['amount'])
        type = request.POST['type']
        details = request.POST['details']
        collaborate_farms = request.POST.getlist('collaborate_farms')
        collaborate_farms.append(farm_id)
        len_collaborate_farms = len(collaborate_farms)
        split_amount = amount // len_collaborate_farms
        remaining_amount = amount  # Track remaining amount for the last farm
        for farm in collaborate_farms:
            if farm == collaborate_farms[-1]:
                split_amount = remaining_amount  # Assign remaining amount to the last farm
            if type == 'income':
                Income.objects.create(farm_id=farm, amount=split_amount, details=details)
            else:
                Expenditure.objects.create(farm_id=farm, amount=split_amount, details=details)
            remaining_amount -= split_amount
        return redirect('farm_detail', farm_id=farm_id)

@login_required(login_url='login')
def txnHistory(request):
    # Get income and expenditures only for the logged-in farmer
    inc = Income.objects.filter(farm__farmer=request.user.farmer)
    exp = Expenditure.objects.filter(farm__farmer=request.user.farmer)
    transactions = list(chain(inc, exp))
    
    detailed_transactions = []
    for txn in transactions:
        farm = txn.farm  # Use the related farm directly instead of another query
        txn_type = 'income' if isinstance(txn, Income) else 'expense'
        detailed_transactions.append({
            'date': txn.date,
            'crop': farm.crop_name,
            'farm': farm.farm_name,
            'type': txn_type,
            'amount': txn.amount,
            'details': txn.details
        })
    
    context = {'transactions': detailed_transactions}
    return render(request, 'txnHistory.html', context)

@login_required(login_url='login')
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, farm__farmer=request.user.farmer)
    farm_id = income.farm.id
    income.delete()
    return redirect('farm_detail', farm_id=farm_id)

@login_required(login_url='login')
def delete_expenditure(request, expenditure_id):
    expenditure = get_object_or_404(Expenditure, id=expenditure_id, farm__farmer=request.user.farmer)
    farm_id = expenditure.farm.id
    expenditure.delete()
    return redirect('farm_detail', farm_id=farm_id)

@login_required(login_url='login')
def edit_transaction(request, transaction_id, transaction_type):
    if transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id, farm__farmer=request.user.farmer)
    elif transaction_type == 'expenditure':
        transaction = get_object_or_404(Expenditure, id=transaction_id, farm__farmer=request.user.farmer)
    else:
        return redirect('farm_detail')

    if request.method == 'POST':
        transaction.amount = request.POST['amount']
        transaction.details = request.POST['details']
        transaction.save()
        return redirect('farm_detail', farm_id=transaction.farm.id)

    context = {
        'transaction': transaction,
        'transaction_type': transaction_type
    }
    return render(request, 'edit_transaction.html', context)
