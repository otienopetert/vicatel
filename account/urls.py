from django.urls import path
#from django.urls import include, re_path
from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
   path('', views.index, name="index"),
   path('aboutus/', views.aboutus, name="aboutus"),
   path('signin/', views.signin, name="signin"),
   path('signup/', views.signup, name="signup"),
   path('logout/', views.logoutUser, name="logout"),
   path('confirm-email/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm-email'),
]