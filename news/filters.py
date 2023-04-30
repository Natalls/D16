from django_filters import FilterSet, DateTimeFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    post_time = DateTimeFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                lookup_expr='date__gt',)
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }
