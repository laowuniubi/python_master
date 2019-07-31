import random # 随机数
import string # 字符的
# 引入绘图的包
from PIL import Image,ImageDraw,ImageFont,ImageFile
# 引入缓存的包
from django.core.cache import cache
from uuid import uuid4


# 定义验证码的类
class Captcha(object):
    # 选用的字体的路径
    font_path = 'Monaco.ttf'
    # 生成几位数的验证码
    number = 4
    # 生成验证码图片的宽度与高度
    size = (100,30)
    # 背景颜色,默认是白色
    bgcolor = (255,255,255)
    # 字体颜色，默认为蓝色
    fontcolor = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    # 验证码字体大小
    fontsize = 25
    # 干扰线的颜色，默认是红色
    linecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # 是否要加入干扰线
    draw_line = True
    # 是否绘制干扰点
    draw_point = True
    # 加入干扰线的条数
    line_number = 2

    # 定义一个类方法
    # 用来随机生成一个字符串(包括英文和数字)
    @classmethod
    def __gene_text(cls):
        source = list(string.ascii_letters)
        for index in range(0,10):
            source.append(str(index))
        # 随机获取几位数字拼接
        return ''.join(random.sample(source,cls.number))

    # 定义一个类方法绘制干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        # 开始位置
        begin = (random.randint(0,width),random.randint(0,height))
        # 结束位置
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([begin, end], fill=cls.linecolor)

    # 定义一个类方法绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    # 生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size  # 宽和高
        image = Image.new('RGBA', (width, height), cls.bgcolor)  # 创建图片
        font = ImageFont.truetype(cls.font_path, cls.fontsize)  # 验证码的字体
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = cls.__gene_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.fontcolor)  # 填充字符串
        # 如果需要绘制干扰线
        if cls.draw_line:
            # 遍历line_number次,就是画line_number根线条
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)
        # 如果需要绘制噪点
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)
        # 保存到缓存中，过期时间为2分钟
        uuid = uuid4()
        cache.set(uuid, text.lower(), 120)
        return uuid, image

    # 验证验证码
    @classmethod
    def check_captcha(cls, uuid, code):
        captcha_cache = cache.get(uuid)
        if captcha_cache and captcha_cache == code.lower():
            # 删除缓存
            cache.delete(uuid)
            return True
        else:
            return False
