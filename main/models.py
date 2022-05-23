from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Post(models.Model):

    title = models.CharField(
        blank=False,
        null=False,
        max_length=100
    )

    body = models.TextField(
        blank=False,
        null=False,
        max_length=1000
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.body) > 1000:
            raise ValidationError('Post body must be less than 1000 chars')
    
    def delete(self, *args, **kwargs):
        raise ValidationError('Posts can not be deleted')


class Comment(models.Model):

    body = models.TextField(
        blank=False,
        null=False,
        max_length=500
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.body
    
    def delete(self, *args, **kwargs):
        raise ValidationError('Posts can not be deleted')


class Upvote(models.Model):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_post_upvote'),
            models.UniqueConstraint(fields=['comment', 'user'], name='unique_comment_upvote'),
        ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='upvotes'
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='upvotes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='upvotes'
    )

    def clean(self):
        if self.post != None and self.comment != None:
            raise ValidationError('Post and comment are exclusive!')
        
        if self.post == None and self.comment == None:
            raise ValidationError('Post or comment are required')

    def delete(self, *args, **kwargs):
        raise ValidationError('Posts can not be deleted')


class Downvote(models.Model):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_post_downvote'),
            models.UniqueConstraint(fields=['comment', 'user'], name='unique_comment_downvote'),
        ]
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='downvotes'
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='downvotes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='downvotes'
    )

    def clean(self):
        if self.post != None and self.comment != None:
            raise ValidationError('Post and comment are exclusive!')
        
        if self.post == None and self.comment == None:
            raise ValidationError('Post or comment are required')

    def delete(self, *args, **kwargs):
        raise ValidationError('Posts can not be deleted')


class Follow(models.Model):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follower_followed')
        ]

    follower = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='followers'
    )

    followed = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='followeds'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        try:
            if self.follower == self.followed:
                raise ValidationError('Can not follow yourself')
        except User.DoesNotExist:
            pass

