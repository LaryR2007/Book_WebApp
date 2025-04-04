from django import forms
from django.utils.http import urlencode
from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Book, Genre, Author
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from books.owner import OwnerListView, OwnerCreateView, OwnerDetailView, OwnerUpdateView, OwnerDeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404

# Create your views here.
class GenreListView(generic.ListView):
    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'

class GenreDetailView(generic.DetailView):
    model = Genre
    template_name = 'books/genre_detail.html'
    context_object_name = 'genre'

class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'rating']

    author = forms.ModelChoiceField(queryset=Author.objects.all())
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())

class BookCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Book
    form_class = BookCreateForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy("books:genre_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Assign the current user as the owner of the book
        return super().form_valid(form)

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    success_url = reverse_lazy("books:genre_list")


class BookDeleteView(OwnerDeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    context_object_name = 'book'
    fields = '__all__'
    success_url = reverse_lazy("books:genre_list")  # Redirect after successful deletion

class BookUpdateView(OwnerUpdateView):
    model = Book
    fields = ['title', 'author', 'genres', 'rating']
    template_name = 'books/book_form.html'
    context_object_name = 'book'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})
    
class AuthorCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Author
    fields = ['name']
    template_name = 'books/author_form.html'
    fields = '__all__'
    success_url = reverse_lazy("books:genre_list")  # Redirect to the list of authors after successful creation

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the current logged-in user
        return super().form_valid(form)
    
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'
    fields = '__all__'
    success_url = reverse_lazy("books:genre_list")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'registration/logout.html')


class DumpPython(View):
    def get(self, req):
        resp = "<pre>\nUser Data in Python:\n\n"
        resp += "Login url: " + reverse('books:login') + "\n"
        resp += "Logout url: " + reverse('books:logout') + "\n\n"

        if req.user.is_authenticated:
            resp += "User " + req.user.username + "\n"
        else:
            resp += "User is not logged in\n"
        
        resp += """<a href="/books">Go back</a>"""
        return HttpResponse(resp)

class ManualProtect(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'books/authentication.html')
        loginurl = reverse('login')+'?'+urlencode({'next': request.path})
        return redirect(loginurl)
    
class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'books/authentication.html')
        