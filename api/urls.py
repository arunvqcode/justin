
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from api.views import registration_view,login_view,logout_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('Signup/', registration_view, name='signup'),
    path('logout/', logout_view, name='logout'),

   

]