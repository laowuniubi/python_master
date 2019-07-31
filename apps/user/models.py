from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core import validators
from tools.my_validators import userNameMaxLengthValidator, userNameMinLengthValidator, telephoneValidator

# Create your models here.
# Create your models here.
# 该文件用于表示所有用户模型


class UserManager(BaseUserManager):
    use_in_migrations = True
    #  对于UserModel进行额外的验证，此项目验证交由form进行


class UserModel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=10, validators=[userNameMaxLengthValidator, userNameMinLengthValidator], null=False, unique=True)
    email = models.EmailField(null=True, unique=True)
    icon = models.FileField(upload_to='images', default='default.jpg')
    telephone = models.CharField(max_length=11, validators=[telephoneValidator], unique=True)
    date_join = models.DateTimeField(auto_now_add=True,
                                     validators=[validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'], message='不支持的图片格式')])
    # is_superuser = models.BooleanField()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

