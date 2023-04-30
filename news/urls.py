from django.urls import path
from .views import NewsList, NewsDetail, PostSearch, NewsCreate, ArtCreate, NewsUpdate, ArtUpdate, NewsDelete, ArtDelete, CategoryListView, subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(NewsList.as_view()), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArtCreate.as_view(), name='art_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', ArtUpdate.as_view(), name='art_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]