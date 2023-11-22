from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    path('add_user/', views.add_user, name="add-user"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('perfil/', views.view_profile, name="user_profile"),
    path('perfil/mudar-perfil/', views.change_user_profile, name="change_profile"),
    path('perfil/mais-informações/', views.more_info, name="+info"),
    path('perfil/alterar-senha/', views.change_password, name="change_password"),

    # Above, Recovery Password System:
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/done/',
         views.password_reset_done, name='password_reset_done'),
    path('password-reset/complete/',
         views.password_reset_complete, name='password_reset_complete'),
]
