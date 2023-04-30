from celery import shared_task
from django.template.loader import render_to_string
from news.models import Post, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import datetime


@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = instance.category.all()
    subscribers: list[str] = []
    for cat in categories:
        subscribers += cat.subscribers.all()

    subscribers = [s.email for s in subscribers]
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.post_text[:124] + '...',
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=tittle,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def daily_post():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    categories = set(posts.values_list('category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Публикации за последнюю неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
