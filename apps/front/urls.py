from django.urls import path
from django.conf.urls import url

from . import views
from apps.user.student_views import LoginView, RegisterView, LogOutView, ChangeInfoView1,ChangeLogo,ChangeInfoView,Telephone_home,Telephone_login,Telephone_send,Pachong,Pachong1
# from apps.user.student_views import get_identifyCode
from apps.user import student_views

app_name = 'front'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('change_info/', ChangeInfoView.as_view(), name='change_info'),
    path('change_info1/', ChangeInfoView1.as_view(), name='change_info1'),
    path('change_logo/', ChangeLogo.as_view(), name='change_logo'),
    path('telephone_home/', Telephone_home.as_view(), name='telephone_home'),
    path('telephone_login/', Telephone_login.as_view(), name='telephone_login'),
    path('telephone_send/', Telephone_send.as_view(), name='telephone_send'),
    path('pachong/', Pachong.as_view(), name='pachong'),
    path('pachong1/', Pachong1.as_view(), name='pachong1'),
    path('home_view/', views.HomeView.as_view(), name='home_view'),
    path('renren/', views.RenrenView.as_view(), name='renren'),
    path('qzone/', views.QzoneView.as_view(), name='qzone'),
]