from django import forms
from apps.user.models import UserModel
from tools.tool_form import ErrorInfoForm
from tools.password_tools import my_make_password, my_check_password

from tkinter import messagebox
from django.contrib import messages
import tkinter.messagebox
from tkinter import *
import win32api,win32con

# messages.debug(request, '%s SQL statements were executed.' % count)
# # messages.info(request, 'Three credits remain in your account.')
# # messages.success(request, 'Profile details updated.')
# # messages.warning(request, 'Your account expires in three days.')
# # messages.error(request, 'Document deleted.')




"""
此文件由模型表单组成
表单功能：提供表单、关联模型、表单提交验证、表单额外功能验证
（即对于登录表单而言，将会验证用户名是否存在、密码是否错误、账户是否激活）
（对于注册表单而言，将验证name、email、telephone等唯一字段是否存在）
"""


class RegisterForm(forms.ModelForm, ErrorInfoForm):
    pwd1 = forms.CharField(widget=forms.PasswordInput)
    pwd2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        pwd1 = self.cleaned_data.get('pwd1')
        pwd2 = self.cleaned_data.get('pwd2')
        self.cleaned_data.pop('pwd1')
        self.cleaned_data.pop('pwd2')
        if 'captcha' in self.cleaned_data.keys():
            self.cleaned_data.pop('captcha')
        if pwd1 != pwd2:
            print("这是一个弹出提示框")

            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '两次密码输入不一致')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'两次密码输入不一致', u'提示', win32con.MB_OK)
            raise forms.ValidationError("两次密码输入不一致")
        self.cleaned_data['password'] = my_make_password(pwd1)
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if UserModel.check(name=name):
            print("这是一个弹出提示框")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '用户名已被注册')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'用户名已被注册', u'提示', win32con.MB_OK)
            raise forms.ValidationError('用户名已被注册')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email):
            print("这是一个弹出提示框")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '邮箱已被注册')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'邮箱已被注册', u'提示', win32con.MB_OK)
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if UserModel.objects.filter(telephone=telephone):
            print("这是一个弹出提示框")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '手机号已被注册')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'手机号已被注册', u'提示', win32con.MB_OK)
            raise forms.ValidationError('手机号已被注册')
        return telephone

    class Meta:
        model = UserModel
        fields = ['name', 'email', 'telephone']
        error_messages = {
            'name': {
                'required': '请输入用户名',
            },
            'pwd1': {
                'required': '请输入密码',
            },
            'pwd2': {
                'required': '请输入密码',
            },
            'email': {
                'required': '请输入邮箱',
                'invalid': '请输入正确格式的邮箱',
            },
            'telephone': {
                'required': '请输入手机号',
            }
        }


class LoginForm(forms.ModelForm, ErrorInfoForm):

    def clean(self):
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        users = UserModel.objects.filter(name=name)
        if not users:
            # print("这是一个弹出提示框")
            # messagebox.showinfo("提示", "该用户不存在")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '该用户不存在')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'该用户不存在', u'提示', win32con.MB_OK)
            raise forms.ValidationError('该用户不存在')
        if not my_check_password(password=password, hash_password=users[0].password):
            print("这是一个弹出提示框")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '密码错误')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'密码错误', u'提示', win32con.MB_OK)
            raise forms.ValidationError('密码错误')

        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = ['name', 'password']
        error_messages = {
            'name': {
                'required': '请输入用户名',
            },
            'password': {
                'required': '请输入密码',
            },
        }
class TelephoneLoginForm(forms.ModelForm, ErrorInfoForm):

    def clean(self):
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('telephone')
        # mycode = self.cleaned_data.get('mycode')
        # self.cleaned_data.pop(mycode)
        users = UserModel.objects.filter(telephone=phone).first()
        if not users:
            # print("这是一个弹出提示框")
            # messagebox.showinfo("提示", "该用户不存在")
            # def message_askyesno():
            #     top = tkinter.Tk()  # *********
            #     top.withdraw()  # ****实现主窗口隐藏
            #     top.update()  # *********需要update一下
            #     txt = tkinter.messagebox.showinfo("提示", '该用户不存在')
            #     top.destroy()
            #     return txt
            #
            # message_askyesno()
            win32api.MessageBox(0, u'该用户不存在', u'提示', win32con.MB_OK)
            raise forms.ValidationError('该用户不存在')

        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = ['telephone']
        error_messages = {
            'telephone': {
                'required': '请输入手机号',
            }
        }
class InfoChangeForm(forms.ModelForm, ErrorInfoForm):

    class Meta:
        model = UserModel
        fields = ['icon', 'email', 'telephone']
        error_messages = {
            'name': {
                'required': '请输入用户名',
            },
            'icon': {
                'invalid_extension': '请上传正确格式头像',
            },
            'email': {
                'invalid_extension': '请输入邮箱',
                'invalid': '请输入正确格式的邮箱',
            },
            'telephone': {
                'invalid_extension': '请输入手机号',
            }
        }
class ImageChangeForm(forms.ModelForm, ErrorInfoForm):

    class Meta:
        model = UserModel
        fields = ['icon']
        error_messages = {
            'icon': {
                'invalid_extension': '请上传正确格式的图片'
            }
        }
class TelephoneForm(forms.ModelForm, ErrorInfoForm):

    class Meta:
        model = UserModel
        fields = ['telephone']
        error_messages = {
            'telephone': {
                'invalid_extension': '请输入正确手机号'
            }
        }
class ManagerForm(forms.ModelForm, ErrorInfoForm):
    def clean(self):
        users = UserModel.objects.all()
        for user in users:
            print("form:",user)
        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = '__all__'
# class ManagerWarnForm(forms.ModelForm, ErrorInfoForm):
#     def clean(self):
#         users = UserModel.objects.all()
#         for user in users:
#             print("form:", user)
#         return self.cleaned_data
#     class Meta:
#         model = UserModel
#         fields = '__all__'
