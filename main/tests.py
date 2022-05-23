from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from main.forms import PostForm
from main.models import Post, Comment, Upvote, Downvote, Follow
from django.contrib.auth.models import User


class PostTest(TestCase):

    def test_if_title_field_has_at_most_100_chars(self):
        test_user = User.objects.create_user(username='test', password='secret')
        long_title = 'a' * 101
        test_post = Post(title=long_title, body='test', user=test_user)
        with self.assertRaises(ValidationError):
            test_post.full_clean()

    def test_if_body_field_has_at_most_1000_chars(self):
        test_user = User.objects.create_user(username='test', password='secret')
        long_body = 'a' * 1001
        test_post = Post(title='test', body=long_body, user=test_user)
        with self.assertRaises(ValidationError):
            test_post.full_clean()

    def test_if_created_at_is_defined_automatically(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        self.assertIsNotNone(test_post.created_at)
    
    def test_str(self):
        test_user = User.objects.create_user(username='test', password='secret')
        post = Post(title='test', body='test', user=test_user)
        self.assertEqual(str(post), 'test')

    def test_if_user_is_required(self):
        test_post = Post(title='test', body='test', user=None)
        with self.assertRaises(ValidationError):
            test_post.full_clean()

    def test_if_post_can_not_be_deleted(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        with self.assertRaises(ValidationError):
            test_post.delete()


class CommentTest(TestCase):
    
    def test_if_body_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment(post=test_post, body=None, user=test_user)
        with self.assertRaises(ValidationError):
            test_comment.full_clean()

    def test_if_user_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment(post=test_post, body='test', user=None)
        with self.assertRaises(ValidationError):
            test_comment.full_clean()

    def test_if_created_at_is_required(self):
        pass # Django ensure that this field is created

    def test_if_post_field_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_comment = Comment(post=None, body='test', user=test_user) # only in memory
        with self.assertRaises(ValidationError):
            test_comment.full_clean()

    def test_if_body_field_has_at_most_500_chars(self):
        test_user = User.objects.create_user(username='test', password='secret')
        long_body = 'a' * 501
        test_comment = Comment(body=long_body, post=None, user=test_user)
        with self.assertRaises(ValidationError):
            test_comment.full_clean()

    def test_if_created_at_is_defined_automatically(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment(body='test', post=test_post, user=test_user)
        test_comment.save()
        self.assertIsNotNone(test_comment.created_at)

    def test_str(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment(body='test', post=test_post, user=test_user)
        self.assertEqual(str(test_comment), 'test')
    
    def test_if_comment_can_not_be_deleted(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment.objects.create(post=test_post, body='test', user=test_user)
        with self.assertRaises(ValidationError):
            test_comment.delete()


class UpvoteTest(TestCase):

    def test_if_post_or_comment_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_upvote = Upvote(post=None, comment=None, user=test_user)
        with self.assertRaises(ValidationError):
            test_upvote.full_clean()

    def test_if_user_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_upvote = Upvote(post=test_post, user=None)
        with self.assertRaises(ValidationError):
            test_upvote.full_clean()

    def test_if_created_at_is_required(self):
        pass # Django ensures that created_at is set

    def test_if_post_and_comment_are_exclusive(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment.objects.create(body='test', post=test_post, user=test_user)
        test_upvote = Upvote(post=test_post, comment=test_comment, user=test_user)
        with self.assertRaises(ValidationError):
            test_upvote.full_clean()
    
    def test_if_created_at_is_defined_automatically(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_upvote = Upvote.objects.create(post=test_post, user=test_user)
        self.assertIsNotNone(test_upvote.created_at)

    def test_if_upvote_can_not_be_deleted(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_upvote = Upvote.objects.create(post=test_post, user=test_user)
        with self.assertRaises(ValidationError):
            test_upvote.delete()

    def test_if_user_can_not_upvote_the_same_post_more_than_once(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        Upvote.objects.create(post=test_post, user=test_user)
        with self.assertRaises(ValidationError):
            duplicated_upvote = Upvote(post=test_post, user=test_user)
            duplicated_upvote.full_clean()

    def test_if_user_can_not_upvote_the_same_comment_more_than_once(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        # test_comment = Comment.objects.create(body='test', post=test_post, user=test_user)
        test_comment = test_post.comments.create(body='test', user=test_user)
        Upvote.objects.create(comment=test_comment, user=test_user)
        with self.assertRaises(ValidationError):
            duplicated_upvote = Upvote(comment=test_comment, user=test_user)
            duplicated_upvote.full_clean()

class DownvoteTest(TestCase):
    
    def test_if_post_or_comment_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_downvote = Downvote(post=None, comment=None, user=test_user)
        with self.assertRaises(ValidationError):
            test_downvote.full_clean()

    def test_if_user_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_downvote = Downvote(post=test_post, user=None)
        with self.assertRaises(ValidationError):
            test_downvote.full_clean()

    def test_if_post_and_comment_are_exclusive(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_comment = Comment.objects.create(body='test', post=test_post, user=test_user)
        test_downvote = Downvote(post=test_post, comment=test_comment, user=test_user)
        with self.assertRaises(ValidationError):
            test_downvote.full_clean()
    
    def test_if_created_at_is_defined_automatically(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_downvote = Downvote.objects.create(post=test_post, user=test_user)
        self.assertIsNotNone(test_downvote.created_at)

    def test_if_downvote_can_not_be_deleted(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        test_downvote = Downvote.objects.create(post=test_post, user=test_user)
        with self.assertRaises(ValidationError):
            test_downvote.delete()

    def test_if_user_can_not_downvote_the_same_post_more_than_once(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        Downvote.objects.create(post=test_post, user=test_user)
        with self.assertRaises(ValidationError):
            duplicated_downvote = Downvote(post=test_post, user=test_user)
            duplicated_downvote.full_clean()

    def test_if_user_can_not_downvote_the_same_comment_more_than_once(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(title='test', body='test', user=test_user)
        # test_comment = Comment.objects.create(body='test', post=test_post, user=test_user)
        test_comment = test_post.comments.create(body='test', user=test_user)
        Downvote.objects.create(comment=test_comment, user=test_user)
        with self.assertRaises(ValidationError):
            duplicated_downvote = Downvote(comment=test_comment, user=test_user)
            duplicated_downvote.full_clean()


class FollowTest(TestCase):

    def test_if_follower_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_follow = Follow(follower=None, followed=test_user)
        with self.assertRaises(ValidationError):
            test_follow.full_clean()

    def test_if_followed_is_required(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_follow = Follow(follower=test_user, followed=None)
        with self.assertRaises(ValidationError):
            test_follow.full_clean()

    def test_if_created_at_is_defined_automatically(self):
        test_user_1 = User.objects.create_user(username='test 1', password='secret')
        test_user_2 = User.objects.create_user(username='test 2', password='secret')
        test_follow = Follow.objects.create(follower=test_user_1, followed=test_user_2)
        self.assertIsNotNone(test_follow.created_at)

    def test_if_user_can_not_follow_the_same_user_more_than_once(self):
        test_user_1 = User.objects.create_user(username='test 1', password='secret')
        test_user_2 = User.objects.create_user(username='test 2', password='secret')
        Follow.objects.create(follower=test_user_1, followed=test_user_2)
        with self.assertRaises(ValidationError):
            duplicated_follow = Follow(follower=test_user_1, followed=test_user_2)
            duplicated_follow.full_clean()

    def test_if_user_can_not_follow_himself(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_follow = Follow(follower=test_user, followed=test_user)
        with self.assertRaises(ValidationError):
            test_follow.full_clean()
