import base64
import random
import string
from random import randint

from apps.user.check_code import check_code
# from apps.user.check_code import create_validate_code
from PIL import Image, ImageDraw,ImageFont
from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from apps.user.forms import LoginForm, RegisterForm,ImageChangeForm, InfoChangeForm,TelephoneForm,TelephoneLoginForm
from apps.user.models import UserModel
from tools.my_decorator import student_login_require, login_out, info_filtration
from tools.set_context_info import get_context_from_request_by_context
from tools.my_print import my_print
import win32api,win32con
from tools.captcha import Captcha
from io import BytesIO
import json
# Create your views here.

# 以下是学生登录 、注册、注销等类视图，每个类的最后一个方法都是禁止除了已有的方式外的方式访问


class LoginView(View):
    def get(self, request):
        """
        登录页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'front/login.html', context=context)

    def post(self, request):
        """
        登录页面post访问，接受登录表单提交
        表单验证成功则重定向到主页，否则重定向到登录页面的get
        登录成功会在session中存储student_id，存储后将通过student_login_require拦截器验证
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = UserModel.objects.filter(name=login_form.cleaned_data.get('name'))[0]
            auth.login(request, user)
            my_print('用户：{:}登录'.format(user.name))
            request.session['success_info'] = '登录成功'
            return redirect(reverse('front:index'))
        error = login_form.get_first_error()
        request.session['error_info'] = error
        win32api.MessageBox(0, error, u'提示', win32con.MB_OK)
        return redirect(reverse('front:login'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class LogOutView(View):
    @login_out
    def get(self, request):
        """
        注销页面get访问
        该方法将会清空session（该部分将会在拦截器login_out中实现）
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        infos = request.session.get('infos')
        context = {}
        return render(request, 'front/index.html', context=context)

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class RegisterView(View):
    def get(self, request):
        """
        注册页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        register_form = RegisterForm()
        context = {'form': register_form}
        return render(request, 'front/register.html', context=context)

    def post(self, request):
        """
        注册页面的post访问
        接收注册表单的请求，验证后会写入数据库
        注册成功后重定向到front:index，在session中传递info='注册成功'
        :param request:
        :return:
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = UserModel.objects.create(**form.cleaned_data)
            student.is_superuser = False
            student.save()
            request.session['info'] = '注册成功'
            my_print('用户：{:}注册成功'.format(student.name))
            return redirect(reverse('front:login'))
        else:
            error = form.get_first_error()
            request.session['error_info'] = error
            win32api.MessageBox(0, error, u'提示', win32con.MB_OK)
            return redirect(reverse('front:register'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class ChangeInfoView(View):
    @student_login_require('front:login')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'front/change_info.html', context=context)

    @student_login_require('front:login')
    def post(self, request):
        """
        信息修改页面post访问，接受登录表单提交
        验证成功或失败后都重定向到此class的get访问，返回的信息不同
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        form = InfoChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.telephone = form.cleaned_data.get('telephone')
            user.email = form.cleaned_data.get('email')
            user.save()
            request.session['success_info'] = '修改信息成功'
            win32api.MessageBox(0, u'修改信息成功', u'提示', win32con.MB_OK)

            return redirect(reverse('front:change_info'))
        error = form.get_first_error()
        request.session['error_info'] = error
        win32api.MessageBox(0, error, u'提示', win32con.MB_OK)

        return redirect(reverse('front:change_info'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class ChangeInfoView1(View):
    @student_login_require('front:login')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'front/person.html', context=context)

    @student_login_require('front:login')
    def post(self, request):
        """
        信息修改页面post访问，接受登录表单提交
        验证成功或失败后都重定向到此class的get访问，返回的信息不同
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """
        form = InfoChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.telephone = form.cleaned_data.get('telephone')
            user.email = form.cleaned_data.get('email')
            user.save()
            request.session['success_info'] = '修改信息成功'
            print("这是一个弹出提示框")
            win32api.MessageBox(0, u'修改信息成功', u'提示', win32con.MB_OK)
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示",'修改信息成功')
            #     top.destroy()
            #     return txt
            # message_askyesno()
            return redirect(reverse('front:index'))
        error = form.get_first_error()
        request.session['error_info'] = error
        return redirect(reverse('front:change_info'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class ChangeLogo(View):
    @student_login_require('front:login')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'front/change_logo.html', context=context)

    @student_login_require('front:login')
    def post(self, request):
        """
        信息修改页面post访问，接受登录表单提交
        验证成功或失败后都重定向到此class的get访问，返回的信息不同
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象获取，render()
        """

        # def post(self, request):
        #     form = ArticleForm(request.POST, request.FILES)
        #     if form.is_valid():
        #         form.save()
        #         return HttpResponse("ok")
        #     else:
        #         print(form.errors.get_json_data())
        #         return HttpResponse("fail")
        form = ImageChangeForm(request.POST,request.FILES)
        if form.is_valid():
            icon = form.cleaned_data["icon"]
            print(type(icon))
            # user = request.user
            request.user.icon = icon
            request.user.save()
            request.session['success_info'] = '修改头像成功'
            print("这是一个弹出提示框")

            # def post(self, request):
            #     image_form = UploadImageForm(request.POST, request.FILES)
            #     if image_form.is_valid():
            #         image = image_form.cleaned_data["image"]
            #         request.user.image = image
            #         request.user.save()
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示",'修改头像成功')
            #     top.destroy()
            #     return txt
            # message_askyesno()
            win32api.MessageBox(0, u'修改头像成功', u'提示', win32con.MB_OK)
            return redirect(reverse('front:change_info1'))
        error = form.get_first_error()
        request.session['error_info'] = error
        print("这是一个弹出提示框")
        win32api.MessageBox(0, error, u'提示', win32con.MB_OK)

        # def message_askyesno():
        #     top = tkinter.Tk()  # *********
        #     top.withdraw()  # ****实现主窗口隐藏
        #     top.update()  # *********需要update一下
        #     txt = tkinter.messagebox.showinfo("提示", error)
        #     top.destroy()
        #     return txt
        # message_askyesno()
        return redirect(reverse('front:change_logo'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
# class GetValidImg(View):
#     def get(self,request):
#         obj = ValidCodeImg()
#         img_data,valid_code = obj.getValidCodeImg()
#         request.session['valid_code'] = valid_code
#         return HttpResponse(img_data)
def get_identifyCode(request):
    img = check_code()# 利用上面的模块得到img对象和验证码code
    code = check_code()
    f = BytesIO()  # 得到写入内存的文件句柄
    img.save(f, "png")  # 写入内存
    data = f.getvalue()  # 从内存中读出
    # 将验证码存在各自的session中，这样做的好处是每个人都有自己的验证码，不会相互混淆（一定不能设为全局变量）
    request.session['keep_str'] = code
    return HttpResponse(data)
class Telephone_home(View):
    def get(self, request):
        return render(request, 'front/telephone.html')

    def post(self, request):
        form = TelephoneForm(request.POST)
        print("Manager_home")
        return redirect(reverse('front:telephone_login'))
    def http_method_not_allowed(self,request):
        return HttpResponse('403')


import requests
def sendMessage(phone):
    code = random.randint(10000,99999)
    key_dict = {

            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "170482",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s"%code,  # 您设置的模板变量，根据实际情况修改
            "key": "b38f23d34ddf262241a9ca71d41248fb",  # 应用APPKEY(应用详细页查询)
        }
    r = requests.get('http://v.juhe.cn/sms/send', params=key_dict)
    # r = requests.get('https://www.baidu.com', params=key_dict)
    if r.status_code == 200:
        return code
    else:
        return 0
class Telephone_send(View):
    def get(self, request):
        return render(request, 'front/telephone.html')

    def post(self, request):
        phone = request.POST.get('phone')
        user = UserModel.objects.filter(telephone=phone).first()
        if user:
            request.session['phone'] = phone
            code = sendMessage(phone)
            if code !=0:
                request.session['code'] = code
                win32api.MessageBox(0, u'验证码已经发送', u'提示', win32con.MB_OK)
                return redirect(reverse('front:telephone_login'))
        return redirect(reverse('front:telephone_send'))
class Telephone_login(View):
    def get(self, request):
        form = TelephoneForm()
        context = {'form': form}

        return render(request, 'front/telephone_login.html', context=context)
    def post(self, request):
        phone = request.POST.get("phone")
        # print(telephone)
        mycode = request.POST.get('mycode')
        code = request.session['code']
        user = UserModel.objects.filter(telephone=phone).first()
        if user is None:
            win32api.MessageBox(0, u'用户手机号信息不存在', u'提示', win32con.MB_OK)
            return redirect(reverse('front:telephone_login'))
        else:
            if mycode == str(code):
                request.session['success_info'] = '登录成功'
                return redirect(reverse('front:index'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')

#爬虫
from apps.user.demo2 import get_opener,login_renren,visit_profile
class Pachong(View):
    def get(self, request):
        opener = get_opener()
        login_renren(opener)
        visit_profile(opener)
        return redirect(reverse('front:pachong1'))
    def post(self, request):
        opener = get_opener()
        login_renren(opener)
        visit_profile(opener)
        return redirect(reverse('front:pachong1'))
class Pachong1(View):
    def get(self,request):
        return render(request, 'renren.html')
    def post(self, request):
        return redirect(reverse('front:pachong1'))

