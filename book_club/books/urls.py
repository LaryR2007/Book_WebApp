from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (BookCreateView, GenreListView, GenreDetailView, AuthorCreateView, UserLogoutView)

app_name = 'books'
from django.contrib import admin
urlpatterns = [
    path('', views.GenreListView.as_view(), name='genre_list'),
    path('admin/', admin.site.urls,),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view, name='book_delete'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/<int:pk>/add-book/', views.BookCreateView.as_view(), name='book_create'),
    path('author/new/', views.AuthorCreateView.as_view(), name='author_create'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='books:genre_list'), name='logout'),
]