from django.shortcuts import render
from django.shortcuts import render,redirect
from Auth.models import Register
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
import hashlib
from django.db import transaction, IntegrityError

# username = harsh 
# password = harsh@0501

# Create your views here
def home(request):
    return render(request,'index.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        certificate = request.FILES.get('certificate')

        if not (username and password and certificate):
            return render(request, 'login.html', {'error': 'All fields are required.'})

        # Step 1: Check username + password using Django auth
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

        # Step 2: Verify certificate hash
        try:
            reg = Register.objects.get(user__username=username)
        except Register.DoesNotExist:
            return render(request, 'login.html', {'error': 'User registration record not found.'})

        uploaded_hash = hashlib.sha256(certificate.read()).hexdigest()
        if reg.certificate_hash != uploaded_hash:
            return render(request, 'login.html', {'error': 'Certificate does not match.'})

        # ✅ Both checks passed → login user
        login(request, user)
        return redirect('/profile')

    return render(request, 'login.html')

def registerUser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password')
        certificate = request.FILES.get('certificate')

        if not certificate:
            return render(request, 'register.html', {'error': 'Certificate is required.'})

        # compute hash
        file_bytes = certificate.read()
        cert_hash = hashlib.sha256(file_bytes).hexdigest()
        certificate.seek(0)  # reset file pointer for saving

        # create User + Register in one go
        user = User.objects.create_user(username=username, password=password)
        user.first_name = name or ''
        user.save()

        Register.objects.create(
         user = user,
         phone=phone,
         date=datetime.today(),
         certificate=certificate,
         certificate_hash=cert_hash
        )

    return render(request, 'register.html')

def profileUser(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'profile.html')

def logoutUser(request):
    logout(request)
    return render(request,'index.html')