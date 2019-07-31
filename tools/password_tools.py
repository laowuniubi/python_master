from django.contrib.auth.hashers import make_password, check_password

salt = '123456'  # 加密、核对参数


def my_make_password(password):
    """
    密码哈希
    在原有的基础上增加了salt，将salt独立在此处，便于修改
    :param password: 待加密的明文密码
    :return: 哈希后的密码
    """
    return make_password(password=password, salt=salt)


def my_check_password(password, hash_password):
    """
    密码验证
    用于输入的明文密码和数据库中哈希后的密文做对比
    :param password: 明文密码
    :param hash_password: 数据库存储的哈希后的密码
    :return: 返回True表示密码验证成功，False表示验证失败
    """
    return check_password(password=password, encoded=hash_password)