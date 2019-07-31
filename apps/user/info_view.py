from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from django.views.generic import View
from django.http import HttpResponse
from apps.user.forms import LoginForm, RegisterForm, InfoChangeForm
from apps.user.models import UserModel
from tools.my_decorator import student_login_require, login_out, info_filtration
from tools.set_context_info import get_context_from_request_by_context
from tools.my_print import my_print
from django.contrib.auth.decorators import login_required




