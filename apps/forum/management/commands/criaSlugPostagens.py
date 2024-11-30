from django.core.management.base import BaseCommand
from forum.models import PostagemForum

# Para executar o script, execute o seguinte comando no prompt:
# python manage.py criaSlugPostagens
class Command(BaseCommand):
    help = "Atualizar os slugs das postagens que não possuem slug"

    def handle(self, *args, **options):
        postagens = PostagemForum.objects.all()

        for postagem in postagens:
            postagem.save()
            self.stdout.write(self.style.SUCCESS('Os slugs foram atualizados com sucesso ! ' + postagem.titulo))

        self.stdout.write(self.style.SUCCESS('Todos os slugs foram atualizados com sucesso!'))