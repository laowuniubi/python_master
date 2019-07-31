import json, urllib.request
from urllib.parse import urlencode


def send_telephone_code(number, code):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": "{:}".format(number),  # 接受短信的用户手机号码
        "tpl_id": "xxx",  # 您申请的短信模板ID，根据实际情况修改
        "tpl_value": "#code#={:}".format(code),  # 您设置的模板变量，根据实际情况修改
        "key": "xxx",  # 应用APPKEY(应用详细页查询)
    }
    params = urlencode(params)
    content = urllib.request.urlopen(url).read()
    res = json.loads(content)
    if res:
        error_code = res['error_code']
        print(error_code)
    else:
        print('发送验证码错误')


if __name__ == '__main__':
    # send_telephone_code()
    pass