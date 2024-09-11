from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import author_list, author_create, author_update, author_delete, author_detail
from .api_views import AuthorViewSet


urlpatterns = [
    path("", views.author_list, name="author_list"),
    path("<int:id>/", views.author_detail, name="author_detail"),

    path("create/", views.author_create, name="author_create"),
    path("edit/<int:id>/", views.author_update, name="author_update"),
    path("delete/<int:id>/", views.author_delete, name="author_delete"),
]

