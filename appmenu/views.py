from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout 
from .models import Produto, Carrinho, Categoria, Marca
from .forms import ProdutoForm, CadastroForm
from django.core.paginator import Paginator

# Create your views here.
def login_view(request):  # Renomeado de login para login_view
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 
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
    # Captura o termo de busca
    termo_busca = request.GET.get('q')

    # Filtra os produtos com base no nome (se um termo de busca for fornecido)
    produtos = Produto.objects.all()
    
    if termo_busca:
        produtos = produtos.filter(nome__icontains=termo_busca)  # Filtra por nome do produto

    # Adicionando filtros de categoria e marca, se necessário
    categoria = request.GET.get('categoria')
    marca = request.GET.get('marca')
    if categoria:
        produtos = produtos.filter(categoria__nome=categoria)
    if marca:
        produtos = produtos.filter(marca__nome=marca)

    # Paginação
    paginator = Paginator(produtos, 8)  # Exibe 8 produtos por página
    page = request.GET.get('page')
    produtos = paginator.get_page(page)

    # Recupera as categorias e marcas para o filtro
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    return render(request, 'produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'marcas': marcas,
        'termo_busca': termo_busca,  # Passa o termo de busca para manter no campo de pesquisa
    })
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)

        print(form.data)
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

    

def sobre(request):
    return render(request, 'sobre.html')

@login_required
def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_item, created = Carrinho.objects.get_or_create(
        usuario=request.user, produto=produto
    )
    if not created:
        carrinho_item.quantidade += 1
        carrinho_item.save()
    return redirect('produtos')

@login_required
def alterar_quantidade_carrinho(request, item_id):
    item = get_object_or_404(Carrinho, id=item_id, usuario=request.user)
    
    if request.method == 'POST':
        # Verifica se o botão pressionado foi para aumentar ou diminuir a quantidade
        if 'quantidade' in request.POST:
            # Se o campo 'quantidade' foi enviado (botão +)
            quantidade = int(request.POST['quantidade'])
            if quantidade > 0:
                item.quantidade = quantidade
                item.save()
        else:
            # Caso contrário, diminui a quantidade (botão -)
            item.quantidade -= 1
            if item.quantidade <= 0:
                item.delete()  # Remove o item se a quantidade for <= 0
            else:
                item.save()
                
    return redirect('carrinho')


@login_required
def carrinho(request):
    carrinho_items = Carrinho.objects.filter(usuario=request.user)
    total = sum([item.subtotal() for item in carrinho_items])
    if (request.method == 'POST'):
        carrinho_items.delete()
        messages.success(request, 'Compra realizada com sucesso!')
        return redirect('carrinho')
    return render(request, 'carrinho.html', {'carrinho': carrinho_items, 'total': total})
    
@login_required
def remover_carrinho(request, produto_id):
    carrinho_item = get_object_or_404(Carrinho, usuario=request.user, produto_id=produto_id)
    carrinho_item.delete()
    return redirect('carrinho')
