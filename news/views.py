from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .tasks import notify_about_new_post
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.translation import gettext as

class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_of_news'] = len(Post.objects.all())
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_d.html'
    context_object_name = 'news_d'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj




class NewsCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post',)

    def get_initial(self):
        return {'post_type': 'NE'}
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = 'NE'
        self.object.author = Author.objects.get(user_id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        notify_about_new_post.apply_async([self.object.pk])
        return result


class ArtCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'art_edit.html'
    permission_required = ('news.add_post',)

    def get_initial(self):
        return {'post_type': 'AR'}
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = 'AR'
        self.object.author = Author.objects.get(user_id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        notify_about_new_post.apply_async([self.object.pk])
        return result

class NewsUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)


class ArtUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'art_edit.html'
    permission_required = ('news.change_post',)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    def get_initial(self):
        return {'post_type': 'NE'}

class ArtDelete(DeleteView):
    model = Post
    template_name = 'art_delete.html'
    success_url = reverse_lazy('news_list')
    def get_initial(self):
        return {'post_type': 'AR'}

class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-post_time')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Поздравляем! Вы успешно оформили подписку на категорию'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


