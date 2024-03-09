from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        if ("@" in username_or_email) and password:
            user = authenticate(username= User.objects.get(email=username_or_email), password=password) 
        else:
            user = authenticate( username= username_or_email, password=password) 
        if user is not None:
            login(request, user)
            messages.info(request, f"Hosgeldin {request.user.username}")
            return redirect('post:list')
    context = dict()
    return render(request, "page/login_page.html", context)

def register_view(request):
    context = dict()
    if request.method == "POST":
        errors = []
        email = request.POST.get('email')
        first_name = request.POST.get('full_name').split(" ")[0]
        last_name = request.POST.get('full_name').split(" ")[1]
        username = request.POST.get('username')
        password = request.POST.get('password')
        context['email'] = email
        context['username'] = username
        # if not password == password2:
        #     errors.append("Sifrenizi Dogru Girin..")
        if User.objects.filter(username=username).exists():
            errors.append("Bu kullanici daha once olusturulmus..")
        if len(username) <= 1:
            errors.append("kullanici adi cok kisa..")
        if errors:
            for error in errors:
                messages.warning(request, error)
            return render(request, "page/register_page.html", context)
        user = User.objects.create(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name 
        )
        user.set_password(password)
        user.save()
        messages.success(request, f"Kaydiniz basariyla yapildi. Lutfen giris yapiniz...")
        return redirect('login')
    return render(request, "page/register_page.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "Oturumunuz sonlandirildi..")
    return redirect('login')