from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'profession', 'address')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

         # Putting the inputPassword widget & required validators
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['password_confirmation'] = forms.CharField(widget=forms.PasswordInput())


        # Form control section
        for field in self.fields.values():
            field.widget.attrs.pop('autofocus', None)
            field.widget.attrs['class'] = 'form-control'

        self.fields['photo'].widget.attrs['class'] = 'form-control-file'

        self.fields['cell_phone'].widget.attrs['class'] = 'form-control phone'

        # Placeholder field
        self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Último nome'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Endereço de email'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password_confirmation'].widget.attrs['placeholder'] = 'Confirme sua Senha'
        self.fields['cell_phone'].widget.attrs['placeholder'] = '(DDD)99999-9999'


class UserProfileLoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'password_confirmation')

    def __init__(self, *args, **kwargs):
        super(UserProfileLoginForm, self).__init__(*args, **kwargs)

         # Putting the inputPassword widget & required validators
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['password_confirmation'] = forms.CharField(widget=forms.PasswordInput())


        # Form control section
        for field in self.fields.values():
            field.widget.attrs.pop('autofocus', None)
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password_confirmation'].widget.attrs['placeholder'] = 'Confirme sua Senha'


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'cell_phone', 'photo',)

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['photo'].widget.attrs['class'] = 'form-control-file'
        self.fields['cell_phone'].widget.attrs['class'] = 'form-control phone'

        self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Último nome'
        self.fields['cell_phone'].widget.attrs['placeholder'] = '(DDD)99999-9999'


class MorefeInfoUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profession', 'address')

    def __init__(self, *args, **kwargs):
        super(MorefeInfoUserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = False

        self.fields['profession'].widget.attrs['placeholder'] = 'Full Stack Developer'
        self.fields['address'].widget.attrs['placeholder'] = 'Manaíra, João Pessoa, PB'


class UserPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChange, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True
            field.widget.attrs['class'] = 'form-control'

        self.fields['old_password'].widget.attrs['label'] = 'Senha atual'
        self.fields['new_password1'].widget.attrs['label'] = 'Nova senha'
        self.fields['new_password2'].widget.attrs['label'] = 'Confirme sua nova senha'

        self.fields['old_password'].widget.attrs['placeholder'] = 'Confirme sua senha atual'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Sua nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirme sua nova senha'


class PasswordRecovery(forms.ModelForm):
    password = forms.CharField(label='Nova Senha', widget=forms.PasswordInput(
        attrs={'class': 'form-control passwordinput'}))
    password_confirmation = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput(
        attrs={'class': 'form-control passwordinput'}))

    class Meta:
        model = UserProfile
        fields = ['password', 'password_confirmation']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError('As senhas não coincidem.')

        return password_confirmation

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user_profile.user.set_password(password)

        if commit:
            user_profile.user.save()

        return user_profile.user