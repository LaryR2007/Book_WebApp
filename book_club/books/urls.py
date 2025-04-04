from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (BookCreateView, GenreListView, GenreDetailView, AuthorCreateView, LogoutView)

app_name = 'books'
from django.contrib import admin
urlpatterns = [
    path('', views.GenreListView.as_view(), name='genre_list'),
    path('admin/', admin.site.urls,),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view, name='book_delete'),
    path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/<int:pk>/add-book/', views.BookCreateView.as_view(), name='book_create'),
    path('author/new/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("logout/", views.LogoutView.as_view(), name = "logout"),
]