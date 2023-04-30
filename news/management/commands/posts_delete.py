from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляем все новости выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        category_name = options['category']
        self.stdout.write(f"Вы увернены, что необходимо удалить все новости из категори {category_name} yes/no?")
        answer = input()
        if answer == 'yes':
            posts = Post.objects.filter(categories__name=category_name)
            posts.delete()
            self.stdout.write(self.style.SUCCESS(f"Новости из категории {category_name} удалены!"))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))