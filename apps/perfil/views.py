from django.shortcuts import get_object_or_404, render

from apps.base.utils import filtrar_modelo
from forum.forms import PostagemForumForm
from contas.models import MyUser
from django.core.paginator import Paginator

def perfil_view(request, username):
    filtro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(filtro, username=username)
    
    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas
    filtros = {}
    valor_busca = request.GET.get("titulo") # Pega parametro
    if valor_busca:
        filtros['titulo'] = valor_busca # Adiciono no dicionario
        filtros['descricao'] = valor_busca # Adiciono no dicionario
    
        # Utiliza o modelo das postagens do perfil
        #perfil_postagens = filtrar_modelo(perfil_postagens.model, **filtros)
        # Estou passando o Query set já filtrado, em vez do model
        perfil_postagens = filtrar_modelo(perfil_postagens, **filtros)
        print(f'perfil_view -> perfil_postagens: {perfil_postagens}')
    
    form_dict = {}
    for el in perfil_postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
        
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'perfil.html', context)