from django.urls import path
from .views import index
from .views import other_page, RLogin, RLogout, profile, register, application, profile_bb_delete, profiledone, profileiw, superAdmin


app_name = 'main'

urlpatterns = [
   path('', index, name='index'),
   path('<str:page>/', other_page, name='other'),
   path('accounts/login/', RLogin.as_view(), name='login'),
   path('accounts/logout/', RLogout.as_view(), name='logout'),
   path('accounts/profile/addapplications/', application, name='application'),
   path('accounts/profile/', profile, name='profile'),
   path('accounts/profiledone/', profiledone, name='profiledone'),
   path('accounts/profileiw/', profileiw, name='profileiw'),
   path('accounts/register/', register, name='register'),
   path('accounts/profile/delete/<int:pk>', profile_bb_delete, name='profile_bb_delete'),
   path('accounts/profile/', profile, name='profile'),
   path('accounts/superadmin/', superAdmin, name='superAdmin'),
]
