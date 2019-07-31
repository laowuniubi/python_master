import base64

from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from apps.user.forms import LoginForm, RegisterForm, InfoChangeForm,ImageChangeForm,ManagerForm
from apps.user.models import UserModel
from tools.my_decorator import teacher_login_require, login_out, info_filtration
from tools.set_context_info import get_context_from_request_by_context
from tools.my_print import my_print
import win32api,win32con
from tools.captcha import Captcha
from io import BytesIO
import json

# Create your views here.

# 以下是教师登录 、注册、注销等类视图，每个类的最后一个方法都是禁止除了已有的方式外的方式访问


class LoginView(View):
    def get(self, request):
        """
        登录页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'cms/login.html', context=context)

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
            if user.is_superuser:
                auth.login(request, user)
                my_print('用户：{:}登录'.format(user.name))
                request.session['success_info'] = '登录成功'
                return redirect(reverse('cms:index'))
            else:
                my_print('权限控制，禁止{:}访问'.format(user.name))
                request.session['error_info'] = '您没有访问的权限'
                return redirect(reverse('cms:login'))
        error = login_form.get_first_error()
        win32api.MessageBox(0, u'您没有访问的权限', u'提示', win32con.MB_OK)

        request.session['error_info'] = error
        return redirect(reverse('cms:login'))

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
        return render(request, 'cms/index.html', context=context)

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
        return render(request, 'cms/register.html', context=context)

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
            my_print(form.cleaned_data)
            teacher = UserModel.objects.create(**form.cleaned_data)
            teacher.is_superuser = True
            teacher.save()
            request.session['info'] = '注册成功'
            my_print('教师：{:}注册成功'.format(teacher.name))
            return redirect(reverse('cms:login'))
        else:
            error = form.get_first_error()
            win32api.MessageBox(0, error, u'提示', win32con.MB_OK)

            request.session['error_info'] = error
            return redirect(reverse('cms:register'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')


class ChangeInfoView(View):
    @teacher_login_require('cms:change_info')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'cms/change_info.html', context=context)

    @teacher_login_require('cms:change_info')
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
            return redirect(reverse('cms:change_info1'))
        error = form.get_first_error()
        win32api.MessageBox(0, error, u'提示', win32con.MB_OK)

        request.session['error_info'] = error
        return redirect(reverse('cms:change_info'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class ChangeInfoView1(View):
    @teacher_login_require('cms:login')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'cms/person.html', context=context)

    @teacher_login_require('cms:login')
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
            return redirect(reverse('cms:index'))
        error = form.get_first_error()
        request.session['error_info'] = error
        win32api.MessageBox(0, error, u'提示', win32con.MB_OK)
        return redirect(reverse('cms:change_info'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class ChangeLogo(View):
    @teacher_login_require('cms:login')
    def get(self, request):
        """
        信息修改页面get访问
        :param request:HttpRequest对象
        :return: 返回HttpResponse对象或者render()
        """
        form = InfoChangeForm()
        context = {'form': form}
        return render(request, 'cms/change_logo.html', context=context)

    @teacher_login_require('cms:login')
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
            return redirect(reverse('cms:change_info1'))
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
        return redirect(reverse('cms:change_logo'))

    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class Manager_home(View):
    @teacher_login_require('cms:login')
    def get(self, request):
        return render(request, 'cms/member-list.html')

    @teacher_login_require('cms:login')
    def post(self, request):
        form = ManagerForm(request.POST)
        print("Manager_home")
        if form.is_valid():
            users = UserModel.objects.all()
            for user in users:
                print(user)
        win32api.MessageBox(0, u'搜索成功', u'提示', win32con.MB_OK)
        return redirect(reverse('cms:Member_list'))
    def http_method_not_allowed(self,request):
        return HttpResponse('403')

class Member_list(View):
    @teacher_login_require('cms:login')
    def get(self, request):
        users = UserModel.objects.all()
        # uid = request.GET.get("uid")
        # userinfo=UserModel.objects.get(id=uid)
        # return render(request, 'cms/member-list.html',{"users":users,"userinfo":userinfo})
        return render(request, 'cms/member-list.html',{"users":users})

    @teacher_login_require('cms:login')
    def post(self, request):
        form = ManagerForm(request.POST)
        print("Member_list")
        if form.is_valid():
            users=UserModel.objects.all()
            for user in users:
                print(user)
            # uid = request.GET.get("uid")
            # userinfo = UserModel.objects.get(id=uid)
            # if userinfo.id_superuser:
            #     userinfo.id_superuser="False"
            #     userinfo.save()
        # win32api.MessageBox(0, u'查询成功', u'提示', win32con.MB_OK)
        return redirect(reverse('cms:member_home'))
    def http_method_not_allowed(self,request):
        return HttpResponse('403')
class Member_warn(View):
    @teacher_login_require('cms:login')
    def get(self, request):
        form = ManagerForm()
        context = {'form': form}
        id = request.GET.get("id")
        print(id)
        person = UserModel.objects.filter(id=id).first()
        if person is None:
            win32api.MessageBox(0, u'用户不存在', u'提示', win32con.MB_OK)
        else:
            person.delete()
            win32api.MessageBox(0, u'删除成功', u'提示', win32con.MB_OK)
        return redirect(reverse('cms:member_list'))
    @teacher_login_require('cms:login')
    def post(self, request):
        form = ManagerForm(request.POST)
        if form.is_valid():
            id=request.POST['id']
            print(id)
            person=UserModel.objects.filter(id=id).first()
            if person is None:
                win32api.MessageBox(0, u'用户不存在', u'提示', win32con.MB_OK)
            else:
                person.delete()
        # id = request.POST['id']
        # UserModel.objects.get(id=id).delete()
        # users = UserModel.objects.all()
        # for user in users:
        #     print(user)
        return redirect(reverse('cms:member_warn'))

    def http_method_not_allowed(self, request):
        return HttpResponse('403')
# 删除用户信息视图函数
# def Manager_delete(request):
#     user_id = request.GET.get('user_id')
#     UserModel.objects.filter(id=user_id).delete()
#     return redirect(reverse('cms:Member_list'))
