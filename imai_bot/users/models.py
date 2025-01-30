from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models

from users import constants as c


class CustomUserManager(BaseUserManager):
    """кастомный менеджер пользователей."""

    def create_user(self,
                    username,
                    email,
                    password=None,
                    **extra_fields
                    ):
        extra_fields.setdefault('is_active', True)
        if not username:
            raise ValueError('Пользователь должен иметь username')
        if not email:
            raise ValueError('Пользователь должен иметь email')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('access_to_the_bot', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=c.MAX_LENGTH_USERNAME,
        unique=True,
        help_text=(
            f'Максимальная длина {c.MAX_LENGTH_USERNAME} символов. '
            f'{c.MESSAGE}'
        ),
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=c.MESSAGE,
                code='invalid_username',
            ),
        ],
    )
    email = models.EmailField(max_length=c.EMAIL_LENGTH, unique=True)
    telegram_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(
        max_length=c.MAX_LENGTH_FIRST_NAME,
        blank=True
    )
    last_name = models.CharField(max_length=c.MAX_LENGTH_LAST_NAME, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    access_to_the_bot = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'telegram_id']

    class Meta:
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')

    def __str__(self):
        return self.username

    @classmethod
    def already_use(cls, kwargs):
        username = kwargs.get('username')
        telegram_id = kwargs.get('telegram_id')
        errors = dict()
        if cls.objects.filter(
            username=username).exclude(telegram_id=telegram_id).exists():
            errors['username'] = f'Username {username} уже используется.'
        if cls.objects.filter(
            telegram_id=telegram_id).exclude(username=username).exists():
            errors['telegram_id'] = (
                f'Telegram_id {telegram_id} уже используется.'
            )
        return errors
