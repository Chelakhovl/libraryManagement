from django import forms
from .models import Order
from book.models import Book
from authentication.models import CustomUser



class OrderCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.get_all_ordinary_users_queryset(),
        widget=forms.Select,
        required=False,  # Depending on your requirements, you might need to adjust this
        label='Select User'
    )
    
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select,
        required=True,  # Ensure the book selection is required
        label='Select Book'
    )

    class Meta:
        model = Order
        fields = ['user', 'book']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-select fields if editing an existing order
            self.fields['user'].initial = self.instance.user
            self.fields['book'].initial = self.instance.book

    def save(self, commit=True):
        # Save the Order instance
        order = super(OrderCreateForm, self).save(commit=False)
        if commit:
            order.save()
        return order