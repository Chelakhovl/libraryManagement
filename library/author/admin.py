from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')
    list_filter = ('name', 'surname', 'patronymic')