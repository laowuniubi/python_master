import urllib.request
handler = urllib.request.HTTPHandler(debuglevel=1)
opener = urllib.request.build_opener(handler)
from http import cookiejar


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Cookie": "pgv_pvid=5146724799; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCIDTS%7C17761%7CMCMID%7C71991122967003593260888412583202511071%7CMCAAMLH-1535104600%7C11%7CMCAAMB-1535104600%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1534507000s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17768%7CvVersion%7C2.4.0; pgv_pvi=6441753600; RK=iORgFZkhkT; ptcz=50a7d664f0d2587d5cf3524469b873afbeef308c52bf29456c46be6ead1c1b7a; o_cookie=2287228249; _qpsvr_localtk=0.4073098579462098; pgv_si=s4389455872; pgv_info=ssid=s6389204608; ptisp=ctc; ptui_loginuin=2287228249; uin=o2287228249; skey=@5Yy1z9gS9; p_uin=o2287228249; pt4_token=75t1GpULGzW5DlmmB8OwRYDr2U2m4qc9bko7TY4UF2g_; p_skey=3lv3siwWgYizl3WB-wHJ9zdt*10lRECGVE*fDPLCI-s_; Loading=Yes; qz_screen=1440x900; QZ_FE_WEBP_SUPPORT=1; x-stgw-ssl-info=da2e646b838a84718abc430c28334fd3|0.143|1561708281.157|2|r|I|TLSv1.2|ECDHE-RSA-AES128-GCM-SHA256|42000|N|0"
}
class Qzone():
    def get_opener():
        cookies = cookiejar.CookieJar()
        # cookie处理器, 提取cookie
        cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
        # 创建打开器, 处理cookie
        opener = urllib.request.build_opener(cookie_handler)

        return opener
    def login_qzone(opener):
        url = "http://www.renren.com/Login.do?rf=r&origURL=http%3A%2F%2Fwww.renren.com%2F541197383%2Fprofile"

        req = urllib.request.Request(url,headers=headers)
        response = opener.open(req)


    def visit_profile(opener):
        url = "https://user.qzone.qq.com/673123088"
        reqs = urllib.request.Request(url, headers=headers)
        response = opener.open(reqs)
        with open('templates/qzone.html', 'w', encoding='utf-8') as fp:
            fp.write(response.read().decode('utf-8'))
