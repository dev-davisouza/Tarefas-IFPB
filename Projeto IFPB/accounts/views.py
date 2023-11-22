from django.shortcuts import render, redirect
from .forms import UserProfileForm, ChangeProfileForm, MorefeInfoUserProfileForm, UserPasswordChange, PasswordRecovery
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import UserProfile
from tasks.models import Task
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


def add_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Crie uma instância de User com base nos dados do formulário
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Crie uma instância de UserProfile associada ao usuário criado
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            # Redirecione para uma página de sucesso ou faça algo adequado
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('accounts:add-user')

    else:
        form = UserProfileForm()
    return render(request, 'accounts/add-user.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login feito com sucesso!"))
            return redirect('core:home')

        else:
            messages.error(
                request, ("Erro ao tentar o login! Tente de novo."))
            return redirect('accounts:login')

    else:
        messages.info(request, "Ao fazer login você terá acesso a todas as funcionalidades do site! :D")
        return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('core:home')


def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    tasks = Task.objects.filter(owner=request.user.profile)

    for task in tasks:
        task.progress = task.porcentagem_dias_passados()

    context = {'user_profile': user_profile,
               'tasks': tasks, }

    return render(request, 'accounts/user_profile.html', context)


def change_user_profile(request):
    if request.method == 'POST':
        form = ChangeProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil alterado com sucesso")
            return redirect('accounts:change_profile')
    else:
        form = ChangeProfileForm(instance=request.user.profile)

    context = {'form': form}
    return render(request, 'accounts/change_profile.html', context)


def more_info(request):
    if request.method == 'POST':
        form = MorefeInfoUserProfileForm(
            request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações alteradas com sucesso")
            return redirect('accounts:user_profile')
    else:
        form = MorefeInfoUserProfileForm(instance=request.user.profile)

    return render(request, 'accounts/more_info.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChange(request.user.profile, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso.')
            return redirect('core:home')
        else:
            messages.error(request, 'Credenciais não conferem, por favor tente novamente!')

    form = UserPasswordChange(request.user.profile)
    return render(request, 'accounts/change_password.html', {'form': form})


# Password Recovery logic:
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        if UserProfile.objects.filter(email=email).exists():
            user = UserProfile.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user.user)
            password_reset_link = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm',
                        kwargs={'uidb64': uid, 'token': token})
            )
            assunto = "Redefinição de senha"
            msg = f"Clique no link de confirmação: {password_reset_link}"
            remetente = "projetoifpbpi@gmail.com"
            destinatario = [user.email]
            send_mail(assunto, msg, remetente,
                      destinatario, fail_silently=False)
            return redirect('accounts:password_reset_done')
        else:
            messages.warning(
                request, "Este e-mail não está registrado em nosso sistema.")
            return redirect('accounts:password_reset')
    return render(request, 'accounts/recovery/reset_pass.html')


def password_reset_done(request):
    return render(request, 'accounts/recovery/reset_pass_done.html')


def password_reset_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_profile = UserProfile.objects.get(pk=uid)
    except UserProfile.DoesNotExist:
        return redirect('accounts:password_reset')

    if default_token_generator.check_token(user_profile.user, token):
        if request.method == "POST":
            form = PasswordRecovery(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('accounts:password_reset_complete')
        else:
            form = PasswordRecovery(instance=user_profile)

        context = {'form': form}
        return render(request, 'accounts/recovery/reset_pass_confirm.html', context)

    return redirect('accounts:password_reset')


def password_reset_complete(request):
    return render(request, 'accounts/recovery/reset_pass_complete.html')