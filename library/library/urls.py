from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order.views import OrderViewSet
from authentication.views import UserViewSet, UserOrderViewSet
from author.api_views import AuthorViewSet
from book.api_views import BookViewSet
from rest_framework.authtoken import views


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'order', OrderViewSet)
router.register(r'user/(?P<user_id>\d+)/order', UserOrderViewSet, basename='user-order')
router.register(r'author', AuthorViewSet)
router.register(r'book', BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls'), name="authentication"),
    path('book/', include('book.urls'), name="book"),
    path('author/', include('author.urls'), name="author"),
    path('order/', include('order.urls'), name="order"),


    
    path('api/v1/', include(router.urls)),

    path('api-token-auth/', views.obtain_auth_token)
   
]
