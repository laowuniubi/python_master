from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.http import HttpResponse
from tools.set_context_info import get_context_from_request_by_context
from tools.my_decorator import teacher_login_require, login_out, info_filtration

# Create your views here.


class IndexView(View):
    @teacher_login_require('cms:login')
    @info_filtration  # 该装饰器用于获取那些被重定向到主页前，往session中存入的信息，这些信息将会在主页进行展示
    def get(self, request):
        """
        主页get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        context = {}
        context = get_context_from_request_by_context(request, context)
        return render(request, 'cms/index.html', context=context)

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class ShowView(View):
    @teacher_login_require('cms:login')
    @info_filtration  # 该装饰器用于获取那些被重定向到主页前，往session中存入的信息，这些信息将会在主页进行展示，该拦截器应配合get_context_from_request_by_context()
    def get(self, request):
        """
        show页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        context = {}
        context = get_context_from_request_by_context(request, context)
        return render(request, 'cms/index.html', context=context)

    def http_method_not_allowed(self,request):
        return HttpResponse('403')