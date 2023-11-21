"""Определяет схемы URL для blogs"""

from django.urls import path
from . import views


app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:blogpost_id>/', views.post, name='post'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:blogpost_id>/', views.edit_post, name='edit_post'),
]
