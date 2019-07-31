import string
from random import randint

from django.shortcuts import render
import base64
from apps.user.check_code import ValidCodeImg
from PIL import Image, ImageDraw,ImageFont
from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from apps.user.forms import LoginForm, RegisterForm,ImageChangeForm, InfoChangeForm
from apps.user.models import UserModel
from tools.my_decorator import student_login_require, login_out, info_filtration
from tools.set_context_info import get_context_from_request_by_context
from tools.my_print import my_print
import win32api,win32con
from tools.captcha import Captcha
from io import BytesIO
import json
# Create your views here.
# 返回验证码图片
def verify_image(request, width, height):
    words_count = 4  # 验证码中的字符长度
    width = int(width)  # 图片宽度
    height = int(height)  # 图片高度
    size = int(min(width / words_count, height) / 1.3)  # 字体大小设置
    bg_color = (randint(200, 255), randint(200, 255), randint(200, 255))   # 随机背景色（浅色）
    img = Image.new('RGB', (width, height), bg_color)  # 创建图像
    # 第一个参数是颜色通道，这里使用了RGB通道，还有其他的一些通道，如CMYK之类的，但不用管
    # 第二个参数是由宽高组成的元组，数字
    # 第三个参数是图片的背景色，这里用rgb的颜色显示，例如( 255, 255, 255)，注意这是元组

    font = ImageFont.truetype('arial.ttf', size)  # 导入字体
    # 用到了ImageFont的truetype函数，可以自动查询电脑中的字体
    # 第一个参数是字体名字
    # 第二个参数是字体大小
    # 注意这个是windows系统下默认的字体，其他系统自己找

    draw = ImageDraw.Draw(img)  # # 创建画笔
    # 用到了ImageDraw的Draw函数
    # 有且只有一个参数，就是之前创建的画布

    # text = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = string.digits + string.ascii_letters  # 数字+大写字母
    verify_text = ''
    for i in range(words_count):
        text_color = (randint(0, 160), randint(0, 160), randint(0, 160))  # 确定文字的颜色，要随机的颜色，颜色要比较深
        left = width * i / words_count + (width / 4 - size) / 2  # i为第几个文字
        top = (height - size) / 2

        word = text[randint(0, len(text) - 1)]
        verify_text += word
        draw.text((left, top), word, font=font, fill=text_color)
        # 写字需要使用draw的text方法
        # 第一个参数是一个坐标轴元组，分别是距离左边和上边的距离
        # 第二个参数是要写的字（字符串）
        # 后面的两个参数分别是字体和字体颜色

    for i in range(30):
        text_color = (255, 255, 255)  # 颜色：白色
        left = randint(0, width)  # 位置：随机
        top = randint(0, height)
        draw.text((left, top), '*', font=font, fill=text_color)

    for i in range(5):
        line_color = (randint(0, 160), randint(0, 160), randint(0, 160))  # 颜色：随机
        line = (randint(0, width), randint(0, height), randint(0, width), randint(0, height))  # 位置：头尾都随机
        draw.line(line, fill=line_color)
        # 画线条需要使用draw的line方法
        # 第一个参数是包含了两个坐标的元组，分别是线条一头一尾的坐标
        # 后面的参数是线条的颜色

    del draw

    # StringIO，可以将图片缓存到内存里面，读取后就清空内存
    image_stream = BytesIO()  # 建立一个缓存对象
    # print(image_stream)  # 类似于：<_io.BytesIO object at 0x0000022CE22C00F8>
    img.save(image_stream, 'jpeg')  # 将图片保存到内存中
    # print(img, image_stream.getvalue())
    request.session['verify'] = verify_text  # 保存相应的文字在session里面
    return HttpResponse(image_stream.getvalue(), 'image/jpeg')  # 返回内存中的图片