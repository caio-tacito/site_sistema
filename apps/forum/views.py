import re
from django.contrib import messages  
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from forum import models
from forum.forms import PostagemForumForm
from base.utils import add_form_errors_to_messages

# Lista de Postagens
def lista_postagem_forum(request):
    if request.path == '/forum/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html' # lista de post da rota /forum/
    else: # Essa parte mostra no Dashboard
        user = request.user 
        lista_grupos = ['administrador', 'colaborador']
        template_view = 'dashboard/dash-lista-postagem-forum.html' # template novo que vamos criar 
        if any(grupo.name in lista_grupos for grupo in user.groups.all()) or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            #postagens = models.PostagemForum.objects.filter(ativo=True)
            postagens = models.PostagemForum.objects.all()
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)
            
    # Como existe uma lista de objetos, para aparecer o formulário 
	# correspondente no modal precisamos ter um for
    form_dict = {}
    for el in postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
    context = {'postagens': postagens,'form_dict': form_dict}
    return render(request, template_view, context)

# Formulário para Criar Postagem
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens') # pega as imagens
            if len(postagem_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                forum = form.save(commit=False)
                forum.usuario = request.user
                forum.save()
                for f in postagem_imagens:
                    models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                return redirect('lista-postagem-forum')
        else:
            add_form_errors_to_messages(request, form)
    return render(request, 'form-postagem-forum.html', {'form': form})

# Detalhes da Postagem (ID)
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=postagem)
    context = {'postagem': postagem, 'form': form}
    return render(request, 'detalhe-postagem-forum.html', context)

# Editar Postagem (ID)
@login_required
def editar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ postagem.titulo + ' foi atualizado com sucesso!'

    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != postagem.usuario and not (
        any(grupo.name in lista_grupos for grupo in request.user.groups.all())
		or request.user.is_superuser):
        # Redireciona para uma página de erro ou outra página adequada
        messages.warning(request, 'Seu usuário não tem permissões para acessar essa página.')
        return redirect('lista-postagem-forum')  
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            messages.warning(request, message)
            return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form)
    return JsonResponse({'status': 'Ok'}) # Coloca por enquanto.

# Deletar Postagem (ID)
@login_required 
def deletar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+postagem.titulo+' foi deletado com sucesso!' 
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)
        
        if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('lista-postagem-forum')
        return redirect(redirect_route)

    return JsonResponse({'status':message})