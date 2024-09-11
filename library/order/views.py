from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from library.decorators import role_required
from book.models import Book
from authentication.models import CustomUser
from .models import Order
from .forms import OrderCreateForm
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets
from .serializers import OrderSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from rest_framework import status



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Order.objects.none() 
        
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.has_object_permission(request, instance):
            return Response({"detail": "You do not have permission to access this order."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def has_object_permission(self, request, obj):
        return request.user == obj.user or request.user.is_staff or request.user.is_superuserr




@login_required
def order_list(request):
    if request.user.role == 1:
        orders = Order.get_all()
    else:
        orders = Order.get_user_orders(request.user)
        
    context = {
        "user": request.user,
        "orders": orders,
    }
    
    return render(request, "order/order_list.html", context=context)


def order_create(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data.get("book")
            user = form.cleaned_data.get("user") if request.user.role == 1 else request.user
            plated_end_at = timezone.now() + timedelta(days=30)
            Order.create(book=book, user=user, plated_end_at=plated_end_at)

            return redirect("order_list")
    else:
        users = CustomUser.get_all_ordinary_users()
        books = Book.objects.all()
        form = OrderCreateForm()

    context = {
        "user": request.user,
        "form": form,
        "users": users,
        "books": books,
    }

    return render(request, "order/order_create.html", context)

@role_required(1)
def order_close(request, id):
    Order.delete_by_id(id)
    return redirect("order_list")