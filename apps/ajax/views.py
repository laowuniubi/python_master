import base64
from apps.user import check_code
from PIL import Image, ImageDraw
from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from apps.user.forms import LoginForm, RegisterForm,ImageChangeForm, InfoChangeForm
from apps.user.models import UserModel
from tools.my_decorator import student_login_require, login_out, info_filtration
from tools.set_context_info import get_context_from_request_by_context
from tools.my_print import my_print
import win32api,win32con
from tools.captcha import Captcha
from io import BytesIO
import json

class CaptchaView(View):
    def get(self, request):
        uuid, img = Captcha.gene_code()
        buf = BytesIO()  # 构建一个输入输出流
        img.save(buf, "png")  # 将图片保存到输入输出流,也就是内存中
        bur_str = buf.getvalue()  # 获得输入输出流里面的内容
        # session["Code"] = code   # 将验证码值存储到session中
        data = str(base64.b64encode(bur_str))[1:].strip("'")
        data = json.dumps({'uuid': str(uuid), 'image': data})
        my_print('验证码uuid：'+str(uuid))
        return HttpResponse(data)

    def post(self, request):
        uuid = request.POST.get('uuid')
        my_print('接受验证码uuid：'+uuid)
        code = request.POST.get('code')
        data = {}
        if Captcha.check_captcha(uuid, code):
            data['status'] = 0
            data['info'] = 'success'
        else:
            data['status'] = -1
            data['info'] = 'fail'
        return HttpResponse(json.dumps(data))

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CaptchaView, self).dispatch(*args, **kwargs)
