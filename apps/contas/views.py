from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required

from core import settings
from base.utils import add_form_errors_to_messages, filtrar_modelo
from contas.forms import CustomUserCreationForm, UserChangeForm
from contas.models import MyUser
from perfil.forms import PerfilForm
from perfil.models import Perfil
from contas.permissions import grupo_colaborador_required

# Rota timeout (Desconecta por inatividade)
def timeout_view(request):
    return render(request, 'timeout.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# Mudança de Senha Force (first_login)
@login_required
def force_password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_change_password = False # passa o parametro para False.
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
        #else:
        #    add_form_errors_to_messages(request, form)
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'registration/password_force_change_form.html', context)

#Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            
            #if user.is_authenticated and user.requires_password_change(): # Verifica
            if user.requires_password_change(): # Verifica
                msg = 'Olá '+ user.first_name + ', como você pode perceber atualmente \
                        a sua senha é 123 cadastrado. Recomendamos fortemente \
                        que você altere sua senha para garantir a segurança da sua conta. \
                        É importante escolher uma senha forte e única que não seja fácil de adivinhar. \
                        Obrigado pela sua atenção!' 
                messages.warning(request, msg)
                return redirect('force_password_change') # Vai para rota de alterar senha.
            else:
                return redirect('home')
        else:
            messages.error(request, 'Combinação de e-mail e senha inválida. \
                Se o erro persistir, entre em contato com o administrador do sistema.')

    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

# Registrar
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.is_active = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            Perfil.objects.create(usuario=usuario) # Cria instancia perfil do usuário
            
            # Envia e-mail para usuário
            send_mail( # Envia email para usuario
                'Cadastro Plataforma',
                f'Olá, {usuario.first_name}, em breve você receberá um e-mail de \
                    aprovação para usar a plataforma.',
                settings.DEFAULT_FROM_EMAIL, # De (em produção usar o e-mail que está no settings)
                [usuario.email], # para usuario
                fail_silently=False,
            )
            
            messages.success(request, 'Registrado. Um e-mail foi enviado \
                para administrador aprovar. Aguarde contato')
                        
            #messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            add_form_errors_to_messages(request, form)
    form = CustomUserCreationForm(user=request.user)
    return render(request, "register.html",{"form": form})

# Atualizar Meu usuario
@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# Atualizar Qualquer usuário pelo parametro username
@login_required()
@grupo_colaborador_required(['administrador','colaborador'])
def atualizar_usuario(request, username):
    #user = get_object_or_404(MyUser, pk=user_id)
    user = get_object_or_404(MyUser, username=username)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            usuario = form.save()
            
            if user.is_active: ## se usuario for ativado a gente muda o status para True e envia e-mail
                usuario.is_active = True # muda status para True (Aprovado)
                print(usuario.is_active)
                # Envia e-mail avisando usuário.
                send_mail( # Envia email para usuario
                    'Cadastro Aprovado',
                    f'Olá, {usuario.first_name}, seu e-mail foi aprovado na plataforma.',
                    settings.DEFAULT_FROM_EMAIL, # De (em produção usar o e-mail que está no settings)
                    [usuario.email], # para
                    fail_silently=False,
                )
                messages.success(request, 'O usuário '+ usuario.email +'\
                    foi atualizado com sucesso!')
                return redirect('lista_usuarios')
            
            usuario.save()   
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# Lista Todos usuários do sistema
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request): # Lista Cliente 
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False) 
    return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})


#Lista Todos usuarios do sistema
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request):
    
    #perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False)

    filtros = {}
    valor_busca = request.GET.get("titulo") # Pega parametro
    if valor_busca:
        # Adiciono no dicionario
        filtros['first_name'] = valor_busca
        filtros['last_name'] = valor_busca
        filtros['email'] = valor_busca
    # lista_usuarios = filtrar_modelo(lista_usuarios.model, **filtros)
    # Estou passando o Query set já filtrado, em vez do model
    lista_usuarios = filtrar_modelo(lista_usuarios, **filtros)
    print(f'lista_usuarios -> lista_usuarios: {lista_usuarios}')
    
    paginacao = Paginator(lista_usuarios, 3)
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    context = {'page_obj': page_obj}
    return render(request, 'lista-usuarios.html', context)


# Adicionar Novo Usuário
@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def adicionar_usuario(request):
    user_form = CustomUserCreationForm(user=request.user)
    perfil_form = PerfilForm(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, user=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, user=request.user)

        if user_form.is_valid() and perfil_form.is_valid():
            # Salve o usuário
            usuario = user_form.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            # Crie um novo perfil para o usuário
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
 
            messages.success(request, 'Usuário adicionado com sucesso.')
            return redirect('lista_usuarios')
        else:
            add_form_errors_to_messages(request, user_form)
            add_form_errors_to_messages(request, perfil_form)

    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, "adicionar-usuario.html", context)