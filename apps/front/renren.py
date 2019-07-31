import urllib.request
from http import cookiejar
from urllib import parse

headers = {
    "Referer": "http://www.renren.com/",
    "Origin": "http://www.renren.com",
    "Host": "www.renren.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
class renren():
    def get_opener():
        cookies = cookiejar.CookieJar()
        # cookie处理器, 提取cookie
        cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
        # 创建打开器, 处理cookie
        opener = urllib.request.build_opener(cookie_handler)

        return opener


    def login_renren(opener):
        data = {
            "email": "18779781030",
            "icode": "",
            "origURL": "http://www.renren.com/home",
            "domain": "renren.com",
            "key_id": "1",
            "captcha_type": "web_login",
            "password": "8bdd9a3490a3732468d48969401f5a9ca78b413721e5df5054ab1daea662521f",
            "rkey": "c5c08b36d1daef7b10b7ae3c886850e6",
            "f": "",
        }

        login_url  = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=20196582819"
        reqs = urllib.request.Request(login_url, headers=headers,data=parse.urlencode(data).encode('utf-8'))
        opener.open(reqs)


    def visit_profile(opener):
        url = "http://www.renren.com/971382042/profile"
        reqs = urllib.request.Request(url, headers=headers)
        response = opener.open(reqs)
        with open('templates/renren.html', 'w', encoding='utf-8') as fp:
            fp.write(response.read().decode('utf-8'))