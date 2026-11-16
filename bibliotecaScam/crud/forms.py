# biblioteca/forms.py
from datetime import date, timedelta
from django import forms
from .models import Livro, Emprestimo, Resenha


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'data_lancamento',
                  'genero', 'imagem_cip']
        widgets = {
            'data_lancamento': forms.DateInput(attrs={'type': 'date'}),
        }


class EmprestimoForm(forms.ModelForm):
    dias = forms.IntegerField( min_value=1, initial=7,
                              label='Dias de empréstimo')

    class Meta:
        model = Emprestimo
        fields = ['livro', 'usuario','aluno']

    widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'livro': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            }

    def save(self, commit=True):
        instancia = super().save(commit=False)
        instancia.data_devolucao_prevista = (
            date.today() + timedelta(days=self.cleaned_data['dias'])
        )
        if commit:
            instancia.save()
        return instancia


class ResenhaForm(forms.ModelForm):
    class Meta:
        model = Resenha
        fields = ['resumo', 'nota']
        widgets = {
            'resumo': forms.Textarea(attrs={'rows': 5}),
            'nota': forms.NumberInput(attrs={'step': '0.1',
                                             'min': '0', 'max': '5'}),
        }

    def clean_nota(self):
        nota = self.cleaned_data['nota']
        if not (0 <= nota <= 5):
            raise forms.ValidationError('A nota deve estar entre 0 e 5.')
        return nota