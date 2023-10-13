
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

from api.views import registration_view,login_view,logout_view,journal

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', registration_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('ask_journal/', journal, name='journal'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)