from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from main.forms import (
    UserCreateForm,
    UserLoginForm,
    PostCreateForm,
    PostCommentCreateForm
)
from main.models import (
    Post,
    Comment,
    Upvote,
    Downvote,
    Follow
)


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

    def test_str(self):
        test_user_1 = User.objects.create_user(username='test 1', password='secret')
        test_user_2 = User.objects.create_user(username='test 2', password='secret')
        test_follow = Follow.objects.create(follower=test_user_1, followed=test_user_2)
        self.assertEqual(str(test_follow), 'test 1 → test 2')


class HomeViewTest(TestCase):

    def test_if_returns_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')


class UserListViewTest(TestCase):

    def test_if_renders_user_list(self):
        User.objects.create_user(username='test 1', password='secret')
        User.objects.create_user(username='test 2', password='secret')
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/user/list.html')
        self.assertQuerysetEqual(response.context['user_list'], ['<User: test 1>', '<User: test 2>'], ordered=False)
    
    def test_if_renders_no_user_message(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/user/list.html')
        self.assertContains(response, 'No users')


class UserDetailViewTest(TestCase):

    def test_if_renders_user_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        response = self.client.get(f'/user/{test_user.id}/')
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(response.context['user'], User)
        self.assertEqual(response.context['user'].id, test_user.id)
        self.assertTemplateUsed(response, 'main/user/detail.html')

    def test_if_returns_404_if_user_does_not_exist(self):
        response = self.client.get('/user/9999/')
        self.assertEqual(response.status_code, 404)


class UserCreateViewTest(TestCase):

    def test_if_renders_user_create_page(self):
        response = self.client.get('/user/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserCreateForm)
        self.assertTemplateUsed(response, 'main/user/create.html')

    def test_if_creates_user(self):
        post_data = {'username': 'test', 'password1': 'secret!024', 'password2': 'secret!024'}
        response = self.client.post('/user/create/', post_data)
        self.assertIsInstance(User.objects.get(username='test'), User)
        self.assertRedirects(response, '/user/login/')

    def test_if_does_not_create_user_on_invalid_data(self):
        post_data = {'username': 'test', 'password1': 'secret'}
        response = self.client.post('/user/create/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserCreateForm)
        self.assertFalse(response.context['form'].is_valid())


class UserLoginViewTest(TestCase):
    
    def test_if_renders_login_page(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserLoginForm)
        self.assertTemplateUsed(response, 'main/user/login.html')

    def test_if_logs_user_on_valid_data(self):
        User.objects.create_user(username='test', password='secret!024')
        post_data = {'username': 'test', 'password': 'secret!024'}
        response = self.client.post('/user/login/', post_data)
        # TODO check of the user is logged
        self.assertRedirects(response, '/')

    def test_if_renders_form_error_on_invalid_data(self):
        User.objects.create_user(username='test', password='secret!024')
        post_data = {'username': 'test'}
        response = self.client.post('/user/login/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_if_does_not_log_user_on_invalid_data(self):
        User.objects.create_user(username='test', password='secret!024')
        post_data = {'username': 'test', 'password': 'bogus!024'}
        response = self.client.post('/user/login/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class UserLogoutViewTest(TestCase):
    pass


class PostListViewTest(TestCase):
    
    def test_if_renders_posts_list(self):
        test_user = User.objects.create_user(username='test', password='secret')
        Post.objects.create(user=test_user, title='test 1', body='test')
        Post.objects.create(user=test_user, title='test 2', body='test')
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/post/list.html')
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: test 1>', '<Post: test 2>'], ordered=False)
    
    def test_if_renders_no_posts_message(self):
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/post/list.html')
        self.assertContains(response, 'No posts')


class PostDetailViewTest(TestCase):

    def test_if_renders_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        response = self.client.get(f'/post/{test_post.id}/')
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(response.context['post'], Post)
        self.assertEqual(response.context['post'].id, test_post.id)
        self.assertIsInstance(response.context['comment_form'], PostCommentCreateForm)
        self.assertTemplateUsed(response, 'main/post/detail.html')

    def test_if_returns_404_if_post_does_not_exist(self):
        response = self.client.get('/post/9999/')
        self.assertEqual(response.status_code, 404)


class PostCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        response = self.client.get('/post/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_renders_post_create_page(self):
        User.objects.create_user(username='test', password='secret')
        self.client.login(username='test', password='secret')
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostCreateForm)
        self.assertTemplateUsed(response, 'main/post/create.html')

    def test_if_creates_post_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        post_data = {'title': 'test', 'body': 'test', 'user': test_user.id}
        self.client.login(username='test', password='secret')
        response = self.client.post('/post/create/', post_data)
        self.assertIsInstance(Post.objects.get(title='test'), Post)
        created_post = Post.objects.get(title='test')
        self.assertRedirects(response, f'/post/{created_post.id}/')

    def test_if_does_not_create_post_on_invalid_data(self):
        User.objects.create_user(username='test', password='secret')
        post_data = {}
        self.client.login(username='test', password='secret')
        response = self.client.post('/post/create/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostCreateForm)
        self.assertFalse(response.context['form'].is_valid())


class PostCommentCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        post_data = {'body': 'test'}
        response = self.client.post(f'/post/{test_post.id}/comment/create/', post_data)
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_comment_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        post_data = {'body': 'test'}
        self.assertQuerysetEqual(test_post.comments.all(), [])
        self.client.login(username='test', password='secret')
        response = self.client.post(f'/post/{test_post.id}/comment/create/', post_data)
        self.assertQuerysetEqual(test_post.comments.all(), ['<Comment: test>'])
        self.assertRedirects(response, f'/post/{test_post.id}/')

    def test_if_raises_error_if_form_is_invalid(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        post_data = {'body': ''}
        self.client.login(username='test', password='secret')
        with self.assertRaises(ValidationError):
            self.client.post(f'/post/{test_post.id}/comment/create/', post_data)


class PostUpvoteCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        response = self.client.post(f'/post/{test_post.id}/upvote/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_upvote_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        self.assertEqual(test_post.upvotes.count(), 0)
        self.client.login(username='test', password='secret')
        response = self.client.post(f'/post/{test_post.id}/upvote/create/')
        self.assertEqual(test_post.upvotes.count(), 1)
        self.assertRedirects(response, f'/post/{test_post.id}/')


class PostDownvoteCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        response = self.client.post(f'/post/{test_post.id}/downvote/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_downvote_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        self.assertEqual(test_post.downvotes.count(), 0)
        self.client.login(username='test', password='secret')
        response = self.client.post(f'/post/{test_post.id}/downvote/create/')
        self.assertEqual(test_post.downvotes.count(), 1)
        self.assertRedirects(response, f'/post/{test_post.id}/')


class PostCommentUpvoteCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        test_comment = Comment.objects.create(post=test_post, user=test_user, body='test')
        response = self.client.post(f'/post/{test_post.id}/comment/{test_comment.id}/upvote/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_upvote_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        test_comment = Comment.objects.create(post=test_post, user=test_user, body='test')
        self.assertEqual(test_comment.upvotes.count(), 0)
        self.client.login(username='test', password='secret')
        response = self.client.post(f'/post/{test_post.id}/comment/{test_comment.id}/upvote/create/')
        self.assertEqual(test_comment.upvotes.count(), 1)
        self.assertRedirects(response, f'/post/{test_post.id}/')


class PostCommentDownvoteCreateViewTest(TestCase):
    
    def test_if_redirects_if_user_is_not_logged_in(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        test_comment = Comment.objects.create(post=test_post, user=test_user, body='test')
        response = self.client.post(f'/post/{test_post.id}/comment/{test_comment.id}/downvote/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_downvote_and_redirects_to_post_detail(self):
        test_user = User.objects.create_user(username='test', password='secret')
        test_post = Post.objects.create(user=test_user, title='test', body='test')
        test_comment = Comment.objects.create(post=test_post, user=test_user, body='test')
        self.assertEqual(test_comment.downvotes.count(), 0)
        self.client.login(username='test', password='secret')
        response = self.client.post(f'/post/{test_post.id}/comment/{test_comment.id}/downvote/create/')
        self.assertEqual(test_comment.downvotes.count(), 1)
        self.assertRedirects(response, f'/post/{test_post.id}/')


class UserFollowCreateViewTest(TestCase):

    def test_if_redirects_if_user_is_not_logged_in(self):
        followed = User.objects.create_user(username='followed', password='secret')
        response = self.client.post(f'/user/{followed.id}/follow/create/')
        self.assertRedirects(response, '/user/login/')

    def test_if_creates_follow_and_redirects_to_user_detail(self):
        followed = User.objects.create_user(username='followed', password='secret')
        User.objects.create_user(username='follower', password='secret')
        self.assertEqual(followed.followers.count(), 0)
        self.client.login(username='follower', password='secret')
        response = self.client.post(f'/user/{followed.id}/follow/create/')
        self.assertEqual(followed.followers.count(), 1)
        self.assertRedirects(response, f'/user/{followed.id}/')


class UserFollowDeleteViewTest(TestCase):

    def test_if_redirects_if_user_is_not_logged_in(self):
        followed = User.objects.create_user(username='followed', password='secret')
        response = self.client.post(f'/user/{followed.id}/follow/delete/')
        self.assertRedirects(response, '/user/login/')

    def test_if_deletes_follow_and_redirects_to_user_detail(self):
        followed = User.objects.create_user(username='followed', password='secret')
        follower = User.objects.create_user(username='follower', password='secret')
        Follow.objects.create(followed=followed, follower=follower)
        self.assertEqual(followed.followers.count(), 1)
        self.client.login(username='follower', password='secret')
        response = self.client.post(f'/user/{followed.id}/follow/delete/')
        self.assertEqual(followed.followers.count(), 0)
        self.assertRedirects(response, f'/user/{followed.id}/')
