
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from library.decorators import role_required

from order.models import Order
from authentication.models import CustomUser
from author.models import Author
from .models import Book
from .forms import BookCreateForm


@login_required
def book_list(request, id=None):
    query = request.GET.get('query')
    author_id = request.GET.get('author_id')
    user_id = request.GET.get('user_id')
    
    if user_id:
        books = []
        orders = Order.get_user_orders(user_id)
        for order in orders:
            print(order.book.id)
            books.append(order.book)
        books = Book.objects.filter(id__in=[book.id for book in books])  # Convert list to QuerySet
    else:
        books = Book.objects.all()

    if query:
        books = books.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if author_id:
        books = books.filter(authors__id=author_id)

    authors = Author.objects.all()
    ordinary_users = CustomUser.get_all_ordinary_users()

    context = {
        "books": books,
        "authors": authors,
        "user": request.user,
        "ordinary_users": ordinary_users
    }
    if user_id:
        context["selected_user_id"] = user_id
    
    if id:
        context["books"] = [get_object_or_404(Book, id=id)]
        
    return render(request, "book/book_list.html", context=context)


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookCreateForm(request.POST)
        if form.is_valid():
            book = form.save()
            authors = request.POST.getlist("authors")
            if authors:
                authors_objects = Author.objects.filter(id__in=authors)
                book.authors.set(authors_objects)
            return redirect("book_list")
    else:
        form = BookCreateForm()

    context = {
        "form": form,
        "authors": Author.objects.all(),  # Fetch all authors for the form's select field
    }
    return render(request, "book/book_create.html", context)

@login_required
def book_update(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = BookCreateForm(request.POST, instance=book)
        if form.is_valid():
            form_data = form.cleaned_data
            name = form_data.get("name")
            description = form_data.get("description")
            count = form_data.get("count")
            authors = form_data.get("authors")
            if authors:
                authors_objects = Author.objects.filter(id__in=authors)
                book.authors.set(authors_objects)
            book.update(name=name, description=description, count=count)
            # form.save()
            return redirect("book_list", id=book.id)
    else:
        form = BookCreateForm(instance=book)

    context = {
        "form": form,
        "book": book,
        "user": request.user,
    }
    return render(request, "book/book_edit.html", context)


@role_required(1)
def book_delete(request, id):
    book = Book.get_by_id(id)
    book.delete()
    return redirect("book_list")


@login_required
def book_detail(request, id):
    context = {
        "book": Book.get_by_id(id),
        "user": request.user,
    }
    
    return render(request, "book/book_detail.html", context=context)

