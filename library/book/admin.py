from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'count')
    readonly_fields = ('name',)
    search_fields = ('id', 'name', 'description', 'authors')
    list_display = ('name', 'description', 'count',)
    list_filter = ('name', 'description', 'count')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('name',)
        return ()  #
    

