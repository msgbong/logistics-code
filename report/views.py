from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Requisition, Client, Deposit, Engagement
from .forms import RequisitionForm
from django.core.mail import send_mail

def index (request):
    return render(request, 'index.html')

@login_required
def dash (request):
    return render(request, 'dash.html')

def sign(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User(username=username, email=email, password=password)
            user.save()


            return redirect('login') 
    else:
        form = SignupForm()

    return render(request, 'sign.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                return redirect('dash')  # Redirect to dashboard or any other page after login
            else:
                # Authentication failed
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def create_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            requisition = form.save()
            # Send email notification to supervisor
            supervisor_email = requisition.supervisor.email
            send_mail(
                'Requisition Approval Required',
                'A new requisition requires your approval. Login to the system to review it.',
                'noreply@ensibuko.com',
                [supervisor_email],
                fail_silently=False,
            )
            return redirect('review_requisition')  # Redirect to dashboard or any other page
    else:
        form = RequisitionForm()
    return render(request, 'create_requisition.html', {'form': form})

@login_required
def review_requisition(request, requisition_id):
    requisition = Requisition.objects.get(pk=requisition_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            requisition.status = status
            requisition.save()
            if status == 'approved':
                # Send email notification to management
                management_email = 'management@ensibuko.com'  # Replace with actual management email
                send_mail(
                    'Requisition Signed Off',
                    'A requisition has been approved and signed off. Login to the system for details.',
                    'noreply@ensibuko.com',
                    [management_email],
                    fail_silently=False,
                )
            return redirect('dash')  # Redirect to dashboard or any other page
    return render(request, 'review_requisition.html', {'requisition': requisition})