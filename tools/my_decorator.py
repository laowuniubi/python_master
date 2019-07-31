import functools
from django.shortcuts import redirect, reverse
from tools.my_print import my_print
import win32api,win32con

# 我的装饰器


def student_login_require(url_name):
    """
    有参装饰器
    该装饰器用于装饰类方法
    用于装饰类视图的方法
    用于学生登录拦截，未登录的请求将被重定向到url_name
    :param url_name: type:str, value:reverse()的参数, 用于通过name获取url
    :return: 装饰器，返回方法
    """
    def get_fun(func):
        @functools.wraps(func)
        def my_wrapper(self, request, *args, **kwargs):
            user = request.user
            if user.id is None:
                request.session['error_info'] = '您还没有登录，请登录后再访问'
                my_print('未登录拦截')
                #win32api.MessageBox(0, u'未登录拦截', u'提示', win32con.MB_OK)
                return redirect(reverse(url_name))
            if user.is_superuser:
                request.session['error_info'] = '学生页面，您没有权限访问'
                my_print('权限拦截')
                return redirect(reverse(url_name))
            return func(self, request, *args, **kwargs)
        return my_wrapper
    return get_fun


def teacher_login_require(url_name):
    """
    有参装饰器
    该装饰器用于装饰类方法
    用于装饰类视图的方法
    用于学生登录拦截，未登录的请求将被重定向到url_name
    :param url_name: type:str, value:reverse()的参数, 用于通过name获取url
    :return: 装饰器，返回方法
    """
    def get_fun(func):
        @functools.wraps(func)
        def my_wrapper(self, request, *args, **kwargs):
            user = request.user
            if user.id is None:
                request.session['error_info'] = '您还没有登录，请登录后再访问'
                my_print('未登录拦截')
                return redirect(reverse(url_name))
            if not user.is_superuser:
                request.session['error_info'] = '管理员页面，您没有权限访问'
                my_print('权限拦截')
                return redirect(reverse(url_name))
            return func(self, request, *args, **kwargs)
        return my_wrapper
    return get_fun


def login_out(func):
    """
    无参装饰器
    该装饰器用于装饰类方法
    用于装饰类视图
    用于注销用户登录
    :param func: 待装饰的方法
    :return: 装饰器，返回方法对象
    """
    @functools.wraps(func)
    def my_wrapper(self, request, *args, **kwargs):
        request.session.flush()
        my_print('注销登录')
        return func(self, request, *args, **kwargs)
    return my_wrapper


def info_filtration(func):
    """
    无参装饰器
    该装饰器用于装饰类方法
    用于装饰类视图
    用于获取在页面之间重定向时，保存在session中的info、error_info、warming_info、success_info
    获取后将会清除这些info
    :param func: 待装饰的方法
    :return: 装饰器，返回方法对象
    """
    @functools.wraps(func)
    def my_wrapper(self, request, *args, **kwargs):
        session = request.session
        infos = {}
        keys = ['info', 'error_info', 'success_info']
        if 'warming_info' in session.keys():
            session.pop('warming_info')
            raise Exception('发现了放弃的参数')
        for key in keys:
            if key in session.keys():
                infos[key] = session[key]
                session.pop(key)
        request.session['infos'] = infos
        return func(self, request, *args, **kwargs)
    return my_wrapper

