from django.shortcuts import get_object_or_404, render

from forum.forms import PostagemForumForm
from contas.models import MyUser

def perfil_view(request, username):
    filtro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(filtro, username=username)
    
    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
        
    context = {'obj': perfil, 'form_dict': form_dict}
    return render(request, 'perfil.html', context)