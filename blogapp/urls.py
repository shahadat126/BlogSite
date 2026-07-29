from django import urls
from django.urls import path
from .views import Home,posts_list_view
app_name= 'blogapp'
urlpatterns = [
    path('',Home,name='home'),
    path('posts/<int:pk>/',posts_list_view,name='post_details')
]
