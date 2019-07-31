from tools.my_print import my_print


def get_context_from_request_by_context(request, context):
    """
    从request中获取其他页面传递的的信息
    :param request: HttpRequest
    :param context: dict
    :return: dict
    """
    infos = request.session.get('infos')
    if infos:
        request.session.pop('infos')
        context.update(infos)
        my_print(infos)
    return context
