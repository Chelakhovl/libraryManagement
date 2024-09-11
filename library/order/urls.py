from . import views
from django.urls import path, include


urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("close/<int:id>/", views.order_close, name="order_close"),
    
]
