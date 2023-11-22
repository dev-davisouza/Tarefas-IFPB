from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    password_validator = RegexValidator(
        regex=r'^.{8,}$',
        message='A senha deve ter pelo menos 8 caracteres.'
    )
    email_validator = RegexValidator(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'Por favor, insira um endereço de e-mail válido.'
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(
        'Primeiro Nome', max_length=30, null=False, blank=False,  default='')
    last_name = models.CharField(
        'Último Nome', max_length=30, null=False, blank=False, default='')
    username = models.CharField('Nome de Usuário', null=False, blank=False, max_length=150,
                                unique=True, validators=[UnicodeUsernameValidator()], default='')
    email = models.EmailField('Endereço de Email', validators=[
                              email_validator], null=False, blank=False, default='')
    photo = models.ImageField('Foto(opcional)', upload_to='photos', blank=True)
    cell_phone = models.CharField(
        'Celular(opcional)', max_length=16, blank=True)
    password = models.CharField('Senha', max_length=128, validators=[
                                password_validator], null=False, blank=False, default='')
    password_confirmation = models.CharField(
        'Confirmação de Senha', max_length=128, null=False, blank=False, default='')
    profession = models.CharField(
        'Profissão', max_length=100, blank=True, null=True, default='')
    address = models.CharField(
        'Endereço', max_length=200, blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Perfil do usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self):
        return self.user.username


class PasswordResetToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.email}"
