from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'ajax'
urlpatterns = [
    path('captcha/', views.CaptchaView.as_view(), name='captcha'),
]