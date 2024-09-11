from django import forms
from .models import Book
from author.models import Author



class BookCreateForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select Authors'
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-select authors if editing an existing book
            self.fields['authors'].initial = self.instance.authors.all()

    def save(self, commit=True):
        # Save the Book instance first
        book = super(BookCreateForm, self).save(commit=commit)
        if commit:
            # Save the many-to-many data for authors
            self._save_m2m()
        return book