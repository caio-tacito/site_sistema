from django.shortcuts import render
from django.contrib import messages

from pages.models import Blocos

# Create your views here.
def index(request):
    return render(request, 'index.html')


def paginas_view(request):
    url_name = request.resolver_match.url_name
    print(f'paginas_view -> url_name: {url_name}')
    pagina = {
        'home': Blocos.objects.filter(pagina__nome='inicio',ativo=True).order_by('ordem'),
        'sobre': Blocos.objects.filter(pagina__nome='sobre',ativo=True).order_by('ordem'),
        'faq': Blocos.objects.filter(pagina__nome='faq',ativo=True).order_by('ordem'),
        'contato': Blocos.objects.filter(pagina__nome='contato',ativo=True).order_by('ordem'),
        }
    print(f'paginas_view -> pagina[str(url_name)]: {pagina[str(url_name)]}')
    context = {'blocos': pagina[str(url_name)]}
    return render(request, 'index.html', context)