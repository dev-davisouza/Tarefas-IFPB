from django import forms

from .models import Category, Task


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('owner',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})

        self.fields['name'].widget.attrs['placeholder'] = 'Nome da Categoria'
        self.fields['description'].widget.attrs['placeholder'] = 'Descreva sua Categoria...'  # noqa


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('owner', 'created_at', 'completed')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['name'].widget.attrs['placeholder'] = 'Nome da tarefa'
        self.fields['description'].widget.attrs['placeholder'] = 'Descreva sua tarefa...'  # noqa

        # Restringir as categorias ao usuário atualmente logado
        self.fields['category'].queryset = Category.objects.filter(owner=user)


class TaskFilterForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['priority', 'completed']

    priority = forms.ChoiceField(
        label='Prioridade',
        choices=Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    completed = forms.BooleanField(
        label='Concluído',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
