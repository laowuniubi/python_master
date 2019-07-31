from tools.my_print import my_print
# 上下文处理


def info_filtration(request, *args, **kwargs):
    """
    上下文处理器，用于页面交互的信息传递
    在页面重定向时，上一个页面会在session中存入info、error_info、success_info，该上下文处理器会获取session可能存在的info，然后pop，再以字典的形式传递到下一个页面
    此方法被定义为上下文处理器，任何请求都会被过滤掉里面可能存在的info、error_info、success_info，如果需要获取这些信息，请在html中获取
    :param request: HttpRequest
    :param args: (可变长度参数)
    :param kwargs: {字典参数}
    :return: dict
    """
    session = request.session
    print(request.path)
    infos = {}
    keys = ['info', 'error_info', 'success_info']
    print('123')
    for key in keys:
        if key in session.keys():
            infos[key] = session[key]
            session.pop(key)
    return infos

