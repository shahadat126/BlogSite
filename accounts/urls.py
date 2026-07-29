from django.urls import path
from .views import Logout,register_view,Login
app_name='accounts'
urlpatterns = [
    path("login/",Login,name='user_login' ),
    path("logout/",Logout,name='user_logout' ),
    path("register_view/",register_view,name= 'register_view'),
]
