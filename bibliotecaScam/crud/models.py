from django.db import models
# biblioteca/models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    TIPOS = [('aluno', 'Aluno'),
             ('professor', 'Professor'),
             ('servidor', 'Servidor')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='aluno')
    

    def __str__(self):
        nome = self.user.get_full_name() or self.user.username
        return f"{nome} ({self.tipo})"


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100, blank=True)
    data_lancamento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=80, blank=True)
    cdu = models.CharField(max_length=30, blank=True)     # extraído do CIP
    cdi = models.CharField(max_length=30, blank=True)     # extraído do CIP
    imagem_cip = models.ImageField(upload_to='cip/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class Emprestimo(models.Model):
    STATUS = [('ativo', 'Ativo'), ('devolvido', 'Devolvido')]

    # PROTECT garante que livros/usuários não sejam apagados enquanto houver histórico
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='emprestimos')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='emprestimos')
    aluno = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Aluno", default= 1)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='ativo')

    class Meta:
        ordering = ['-data_emprestimo']

    def __str__(self):
        return f"{self.livro.titulo} → {self.usuario.username}"


class Resenha(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='resenhas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenhas')
    resumo = models.TextField()
    nota = models.DecimalField(max_digits=3, decimal_places=1)  # 0.0 a 5.0
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"Resenha de {self.livro.titulo} por {self.usuario.username}"
# Create your models here.
