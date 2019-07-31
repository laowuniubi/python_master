from django.urls import path

from . import views
from apps.user.teacher_views import Member_warn, LoginView, RegisterView, LogOutView, ChangeInfoView,ChangeInfoView1,ChangeLogo,Manager_home,Member_list

app_name = 'cms'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('change_info/', ChangeInfoView.as_view(), name='change_info'),
    path('change_info1/', ChangeInfoView1.as_view(), name='change_info1'),
    path('change_logo/', ChangeLogo.as_view(), name='change_logo'),
    path('manager_home/', Manager_home.as_view(), name='manager_home'),
    path('member_list/', Member_list.as_view(), name='member_list'),
    path('member_warn/', Member_warn.as_view(), name='member_warn'),
    # path('member_warn/',views.Manager_dalete, name='member_warn'),
]