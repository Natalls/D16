from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username}"

    def update_rating(self):
        rating_posts = Post.objects.filter(author_id=self.pk).aggregate(rating=Sum('rating'))['rating']
        rating_comments = Comment.objects.filter(user_id=self.user).aggregate(comment_rating=Sum('comment_rating'))[
            'comment_rating']
        rating_comments_posts = \
            Comment.objects.filter(post__author__user=self.user).aggregate(comment_rating=Sum('comment_rating'))[
                'comment_rating']
        self.user.rating = rating_posts * 3 + rating_comments + rating_comments_posts
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')
    def __str__(self):
        return f"{self.category_name}"


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POST_TYPE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=news)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=20)
    post_text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
