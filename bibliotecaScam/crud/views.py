from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, ResenhaForm
from .utils import extrair_cdu_cdi


# ---------------- LIVROS ----------------

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'crud/lista_livros.html', {'livros': livros})


def novo_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            # OCR na foto da página de CIP
            if livro.imagem_cip:
                try:
                    cdu, cdi = extrair_cdu_cdi(livro.imagem_cip)
                    livro.cdu = cdu
                    livro.cdi = cdi
                except Exception as exc:
                    messages.warning(request, f'Erro no OCR: {exc}')
            livro.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('crud:lista_livros')
    else:
        form = LivroForm()
    return render(request, 'crud/novo_livro.html', {'form': form})


# ---------------- EMPRÉSTIMOS (sem delete) ----------------

def novo_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save()
            _enviar_email_emprestimo(emprestimo)
            messages.success(
                request,
                'Empréstimo registrado e comprovante enviado por e-mail.'
            )
            return redirect('crud:lista_emprestimos')
    else:
        form = EmprestimoForm()
    return render(request, 'crud/novo_emprestimo.html', {'form': form})


def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related('livro', 'usuario')
    return render(request, 'crud/lista_emprestimos.html',
                  {'emprestimos': emprestimos})


def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        emprestimo.status = 'devolvido'
        emprestimo.data_devolucao_real = date.today()
        emprestimo.save()
        _enviar_email_devolucao(emprestimo)
        messages.success(request, 'Devolução registrada.')
        return redirect('crud:lista_emprestimos')
    return render(request, 'crud/devolver_emprestimo.html',
                  {'emprestimo': emprestimo})


# ---------------- RESENHAS ----------------

@login_required
def nova_resenha(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.method == 'POST':
        form = ResenhaForm(request.POST)
        if form.is_valid():
            resenha = form.save(commit=False)
            resenha.livro = livro
            resenha.usuario = request.user
            resenha.save()
            messages.success(request, 'Resenha registrada!')
            return redirect('crud:lista_resenhas', livro_id=livro.id)
    else:
        form = ResenhaForm()
    return render(request, 'crud/nova_resenha.html',
                  {'form': form, 'livro': livro})


def lista_resenhas(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    return render(request, 'crud/lista_resenhas.html', {'livro': livro})


# ---------------- HELPERS DE E-MAIL ----------------

def _enviar_email_emprestimo(emp):
    destino = emp.usuario.email
    if not destino:
        return
    send_mail(
        subject='Comprovante de Empréstimo — Biblioteca Escolar',
        message=(
            f"Olá, {emp.usuario.get_full_name() or emp.usuario.username}!\n\n"
            f"Empréstimo registrado com sucesso.\n\n"
            f"Livro: {emp.livro.titulo}\n"
            f"Autor: {emp.livro.autor}\n"
            f"Data do empréstimo: {emp.data_emprestimo:%d/%m/%Y}\n"
            f"Devolução prevista: {emp.data_devolucao_prevista:%d/%m/%Y}\n\n"
            f"Boa leitura!\nBiblioteca Escolar"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destino],
        fail_silently=True,
    )


def _enviar_email_devolucao(emp):
    destino = emp.usuario.email
    if not destino:
        return
    send_mail(
        subject='Comprovante de Devolução — Biblioteca Escolar',
        message=(
            f"Olá, {emp.usuario.get_full_name() or emp.usuario.username}!\n\n"
            f"Devolução registrada.\n\n"
            f"Livro: {emp.livro.titulo}\n"
            f"Devolvido em: {emp.data_devolucao_real:%d/%m/%Y}\n\n"
            f"Obrigado!\nBiblioteca Escolar"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destino],
        fail_silently=True,
    )
# Create your views here.
