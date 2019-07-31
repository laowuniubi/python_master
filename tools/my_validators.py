from django.core import validators

userNameMinLengthValidator = validators.MinLengthValidator(limit_value=3, message='用户名不能少于3个字符')
userNameMaxLengthValidator = validators.MaxLengthValidator(limit_value=10, message='用户名不能超过10个字符')
telephoneValidator = validators.RegexValidator(regex=r'1[3456789]\d{9}', message='格式错误的手机号')
