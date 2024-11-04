from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login  # Importando o login correto
from .models import Produto
from .forms import ProdutoForm, CadastroForm

# Create your views here.
def login_view(request):  # Renomeado de login para login_view
    return render(request, 'login.html')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # Verifica se o nome de usuário já existe
            if User.objects.filter(username=form.cleaned_data['usuario']).exists():
                messages.error(request, 'Esse nome de usuário já está em uso. Escolha outro.')
                form.add_error('usuario', 'Nome de usuário já em uso')
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['usuario'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['senha']
                )
                auth_login(request, user)  # Agora chamando o login corretamente
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('home')  # Mude para a URL correta após o cadastro
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os dados.')
    else:
        form = CadastroForm()
    
    contexto = {
        'form': form
    }
    
    return render(request, 'cadastro.html', contexto)

def home(request):
    return render(request, 'home.html')


def produtos(request):
    produtos = Produto.objects.all()
    contexto = {
        'produtos': produtos
    }
    return render(request, 'produtos.html', contexto)

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm()
    contexto = {
        'form': form
    }
    return render(request, 'form.html', contexto)

@login_required
@user_passes_test(is_admin)
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)
    contexto = {
        'form': form
    }
    return render(request, 'form.html', contexto)

@login_required
@user_passes_test(is_admin)
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('produtos')
@login_required
def logout_view(request):
    

def sobre(request):
    return render(request, 'sobre.html')

def carrinho(request):
    return render(request, 'carrinho.html')
