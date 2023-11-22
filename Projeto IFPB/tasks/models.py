from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from accounts.models import UserProfile


class Category(models.Model):
    name = models.CharField('Nome', max_length=150)
    description = models.TextField('Descrição', blank=True, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['id']

    def __str__(self):
        return self.name

    def is_owner(self, user):
        return self.owner == user


class Task(models.Model):
    def get_default_dia_de_criacao():
        return timezone.now().date()

    PRIORITY_CHOICES = (
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
    )

    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição', blank=True)
    end_date = models.DateField(
        'Prazo final', auto_now=False, auto_now_add=False)
    created_at = models.DateField(
        default=get_default_dia_de_criacao, editable=False)
    priority = models.CharField(
        'Prioridade', max_length=1, choices=PRIORITY_CHOICES)
    category = models.ManyToManyField(
        Category, verbose_name='Categorias(opcional)', blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def porcentagem_dias_passados(self):
        dias_passados = (timezone.now().date() - self.created_at).days + 1
        total_dias = (self.end_date - self.created_at).days + 1
        return int((dias_passados / total_dias) * 100)

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.enviar_email_tarefa_proxima()

    def enviar_email_tarefa_proxima(self):
        prazo_final = self.end_date
        dias_restantes = (prazo_final - timezone.now().date()).days

        if dias_restantes <= 1:
            assunto = f"A Tarefa {self.name}: Prazo Final Amanhã"
            mensagem = f"A tarefa {self.name} está próxima do prazo final de sua tarefa"
            # Supondo que o atributo "owner" é uma instância do modelo User que representa o responsável pela tarefa
            destinatarios = [self.owner.email]
            remetente = "vlogsplayer10@gmail.com"

            send_mail(assunto, mensagem, remetente,
                      destinatarios, fail_silently=False)
