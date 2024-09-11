from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import CustomUser
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from order.models import Order
from order.serializers import OrderSerializer
from .permissions import IsOwnerOrReadOnly
from library.decorators import role_required



class UserOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Order.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        user = CustomUser.objects.get(pk=user_id)
        serializer.save(user=user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]




def index(request):
    return render(request, "auth/index.html")

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Username or password is incorrect")
    else:
        form = UserLoginForm()
    return render(request, 'auth/login_form.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("index")

def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("user_login")
    else:
        form = UserRegistrationForm()
    return render(request, "auth/register_form.html", {'form': form})

@login_required
def user_delete(request):
    if request.method == "POST":
        user = request.user
        user_id = user.id
        logout(request)
        CustomUser.delete_by_id(user_id)
        messages.success(request, "Your account has been deleted successfully.")
    return redirect("index")

@login_required
def user_account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_account')  
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "user": request.user,
        "form": form  
    }
    return render(request, "auth/account.html", context=context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Your profile has been updated successfully!') 
            return redirect('user_account')  
    else:
        form = UserProfileForm(instance=request.user)  
    
    return render(request, 'auth/account.html', {'form': form})

@role_required(1)  
def all_users(request, id=None):
    if id:
        users = [CustomUser.get_by_id(id)]
    else:
        users = CustomUser.get_all()
    context = {
        "user": request.user,
        "users": users
    }
    return render(request, "auth/all_users.html", context=context)

@role_required(1)  
def user_delete(request, id):
    user = CustomUser.get_by_id(id)
    if user:
        user.delete()
    return redirect("user_list")