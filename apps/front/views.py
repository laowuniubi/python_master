from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.http import HttpResponse
from tools.set_context_info import get_context_from_request_by_context
from tools.my_decorator import student_login_require, login_out, info_filtration
from tools.captcha import Captcha
from io import BytesIO
import json
from apps.front.renren import renren
from apps.front.qqzone import Qzone
# Create your views here.


class IndexView(View):
    # @student_login_require('front:login')
    def get(self, request):
        """
        主页get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        context = {}
        return render(request, 'front/index.html', context=context)

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class ShowView(View):
    @student_login_require('front:login')
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        context = {}
        return render(request, 'front/index.html', context=context)

    def http_method_not_allowed(self):
        return HttpResponse('403')
class HomeView(View):
    @student_login_require('homepage')
    @info_filtration
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        context = {}
        context = get_context_from_request_by_context(request, context)
        return render(request, 'profile-page.html', context=context)

    def http_method_not_allowed(self):
        return HttpResponse('403')

class MoreView(View):
    @student_login_require('')
    @info_filtration
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """

        context = {}
        context = get_context_from_request_by_context(request, context)
        return render(request, '', context=context)

    def http_method_not_allowed(self):
        return HttpResponse('403')


class RenrenView(View):
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        opener = renren.get_opener()
        renren.login_renren(opener)
        renren.visit_profile(opener)
        return render(request, 'renren.html')

    def http_method_not_allowed(self):
        return HttpResponse('403')

class QzoneView(View):
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        opener = Qzone.get_opener()
        Qzone.login_qzone(opener)
        Qzone.visit_profile(opener)
        return render(request, 'qzone.html')

    def http_method_not_allowed(self):
        return HttpResponse('403')