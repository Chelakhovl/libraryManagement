from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("register/", views.user_register, name="user_register"),
    path("delete_account/", views.user_delete, name="user_delete"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    
    path("account/", views.user_account, name="user_account"),
    
    path("users/", views.all_users, name="user_list"),
    path("users/<int:id>/", views.all_users, name="user_list"),
    path("user/delete/<int:id>/", views.user_delete, name="user_delete"),



    path("", views.index, name="index"),
]
