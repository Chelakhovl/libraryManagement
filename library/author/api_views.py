from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Author
from .serializers import AuthorSerializer
from library.decorators import role_required

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    #@role_required(1)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    #@role_required(1)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    #@role_required(1)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    #@role_required(1)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #@role_required(1)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
