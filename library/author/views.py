from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import AuthorForm
from library.decorators import role_required



@role_required(1)
def author_list(request):
    context = {"authors": Author.get_all(), "user": request.user}
    print(context)
    return render(request, "author/author_list.html", context=context)


@role_required(1)
def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm()
    context = {"form": form, "user": request.user}
    return render(request, "author/author_create.html", context=context)


@role_required(1)
def author_update(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm(instance=author)
    context = {"form": form, "author": author, "user": request.user}
    return render(request, "author/author_edit.html", context=context)


@role_required(1)
def author_delete(request, id):
    author = get_object_or_404(Author, id=id)
    author.delete()
    return redirect("author_list")


@login_required
def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    context = {"author": author, "user": request.user}
    return render(request, "author/author_detail.html", context=context)




