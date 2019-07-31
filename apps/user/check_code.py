import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def check_code(width=120, height=30, char_length=5, font_file='../../static/font/Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字符（包括大小写字母和数字）
        :return:
        """
        ranNum = str(random.randint(0, 9))
        ranLower = chr(random.randint(65, 90))
        ranUpper = chr(random.randint(97, 120))
        return random.choice([ranNum, ranLower, ranUpper])

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = ( height - font_size ) / 2
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 对图像加滤波 - 深度边缘增强滤波
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

if __name__ == '__main__':
    # img = check_code()
    # data, valid_str = img.getValidCodeImg()
    # print(valid_str)
    #
    # f = open('test.png', 'wb')
    # f.write(data)
    # 1. 直接打开，即用图片查看器查看
    img,code = check_code()
    img.show()

    # 2. 写入文件
    # img,code = check_code()
    # with open('code.png','wb') as f:   # f是写入磁盘的文件句柄
    #     img.save(f, format='png')
    # data = f.read()   # data是读取图片的字节

    # 3. 写入内存(Python3)
    # img,code = check_code()
    # from io import BytesIO    # 内存管理的模块
    # stream = BytesIO()         # stream是写入内存的文件句柄
    # img.save(stream, 'png')
    # data = stream.getvalue()

    # 4. 写入内存（Python2）
    # img,code = check_code()
    # import StringIO
    # stream = StringIO.StringIO()  # stream是写入内存的文件句柄
    # img.save(stream, 'png')
    # data = stream.getvalue()

# _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
# _upper_cases = _letter_cases.upper()  # 大写字母
# _numbers = ''.join(map(str, range(3, 10)))  # 数字
# init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
#
#
# def create_validate_code(size=(120, 30),
#                          chars=init_chars,
#                          img_type="GIF",
#                          mode="RGB",
#                          bg_color=(255, 255, 255),
#                          fg_color=(0, 0, 255),
#                          font_size=18,
#                          font_type="Monaco.ttf",#依赖字体，需要下载相应的字体文件
#                          length=4,
#                          draw_lines=True,
#                          n_line=(1, 2),
#                          draw_points=True,
#                          point_chance=2):
#     """
#     @todo: 生成验证码图片
#     @param size: 图片的大小，格式（宽，高），默认为(120, 30)
#     @param chars: 允许的字符集合，格式字符串
#     @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
#     @param mode: 图片模式，默认为RGB
#     @param bg_color: 背景颜色，默认为白色
#     @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
#     @param font_size: 验证码字体大小
#     @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
#     @param length: 验证码字符个数
#     @param draw_lines: 是否划干扰线
#     @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
#     @param draw_points: 是否画干扰点
#     @param point_chance: 干扰点出现的概率，大小范围[0, 100]
#     @return: [0]: PIL Image实例
#     @return: [1]: 验证码图片中的字符串
#     """
#
#     width, height = size  # 宽高
#     # 创建图形
#     img = Image.new(mode, size, bg_color)
#     draw = ImageDraw.Draw(img)  # 创建画笔
#
#     def get_chars():
#         """生成给定长度的字符串，返回列表格式"""
#         return random.sample(chars, length)
#
#     def create_lines():
#         """绘制干扰线"""
#         line_num = random.randint(*n_line)  # 干扰线条数
#
#         for i in range(line_num):
#             # 起始点
#             begin = (random.randint(0, size[0]), random.randint(0, size[1]))
#             # 结束点
#             end = (random.randint(0, size[0]), random.randint(0, size[1]))
#             draw.line([begin, end], fill=(0, 0, 0))
#
#     def create_points():
#         """绘制干扰点"""
#         chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
#
#         for w in range(width):
#             for h in range(height):
#                 tmp = random.randint(0, 100)
#                 if tmp > 100 - chance:
#                     draw.point((w, h), fill=(0, 0, 0))
#
#     def create_strs():
#         """绘制验证码字符"""
#         c_chars = get_chars()
#         strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开
#
#         font = ImageFont.truetype(font_type, font_size)
#         font_width, font_height = font.getsize(strs)
#
#         draw.text(((width - font_width) / 3, (height - font_height) / 3),
#                   strs, font=font, fill=fg_color)
#
#         return ''.join(c_chars)
#
#     if draw_lines:
#         create_lines()
#     if draw_points:
#         create_points()
#     strs = create_strs()
#
#     # 图形扭曲参数
#     params = [1 - float(random.randint(1, 2)) / 100,
#               0,
#               0,
#               0,
# - float(random.randint(1, 10)) / 100,
#               float(random.randint(1, 2)) / 500,
#               0.001,
#               float(random.randint(1, 2)) / 500
#               ]
#     img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
#
#     img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
#
#     return img, strs
