from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from main.models import (
    Post,
    Comment
)


class UserCreateForm(UserCreationForm):
    pass


class UserLoginForm(AuthenticationForm):
    pass


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'user']


class PostCommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
