from django import urls
from django.urls import path
from .views import Home,posts_list_view,post_details_view
app_name= 'blogapp'
urlpatterns = [
    path('',Home),
    path('posts/<int:pk>/',post_details_view,name='post_details'),
    path('posts/',posts_list_view,name='posts_list'),
]
