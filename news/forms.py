from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'post_text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is None:
            raise ValidationError({'title': 'Заголовок не может отсутствовать'})
        text = cleaned_data.get('post_text')
        if len(text) < 20:
            raise ValidationError({'post_text': 'Текст не может быть менее 20 символов'})
        elif title == text:
            raise ValidationError({'post_text': 'Текст и заголовок не могут быть одинаковыми'})
        return cleaned_data
