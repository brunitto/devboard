from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from main.forms import (
    PostCommentCreateForm,
    UserCreateForm,
    PostCreateForm,
    UserLoginForm
)
from main.models import (
    Post,
    Comment,
    Upvote,
    Downvote,
    Follow
)


def home_view(request):
    return render(request, 'main/home.html')


def user_list_view(request):
    user_list = User.objects.all()
    return render(request, 'main/user/list.html', {'user_list': user_list})


def user_detail_view(request, id):
    try:
        user = User.objects.get(id=id)
        return render(request, 'main/user/detail.html', {
            'user_model': user
        })
    except User.DoesNotExist:
        raise Http404


def user_create_view(request):

    if request.method == 'GET':
        # create an empty form
        user_create_form = UserCreateForm()
        return render(request, 'main/user/create.html', {'form': user_create_form})
    
    if request.method == 'POST':
        # check if the form is valid
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            user_create_form.save()
            return redirect('/user/login/')
        else:
            # form is invalid!
            return render(request, 'main/user/create.html', {'form': user_create_form})


def user_login_view(request):

    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'main/user/login.html', {
            'form': form
        })
    
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        
        return render(request, 'main/user/login.html', {'form': form})


def user_logout_view(request):
    logout(request)
    return redirect('/')


def post_list_view(request):
    post_list = Post.objects.all()
    return render(request, 'main/post/list.html', {'post_list': post_list})


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    comment_form = PostCommentCreateForm()
    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, 'main/post/detail.html', context)


@login_required(login_url='/user/login/', redirect_field_name=None)
def post_create_view(request):

    if request.method == 'GET':
        post_create_form = PostCreateForm()
        return render(request, 'main/post/create.html', {'form': post_create_form})

    if request.method == 'POST':
        post_create_form = PostCreateForm(request.POST)
        if post_create_form.is_valid():
            post_create_form.save()
            return redirect(f'/post/{post_create_form.instance.id}/')
        else:
            return render(request, 'main/post/create.html', {'form': post_create_form})


@login_required(login_url='/user/login/', redirect_field_name=None)
def post_comment_create_view(request, id):
    
    if request.method == 'POST':
        post_comment_create_form = PostCommentCreateForm(request.POST)
        if post_comment_create_form.is_valid():
            post = Post.objects.get(id=id)
            post_comment_create_form.instance.post = post
            post_comment_create_form.instance.user = request.user
            post_comment_create_form.save()
            return redirect(f'/post/{id}/')
        else:
            raise ValidationError('Comment is invalid!')


@login_required(login_url='/user/login/', redirect_field_name=None)
def post_upvote_create_view(request, id):
    
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        upvote = Upvote(post=post, user=request.user)
        upvote.full_clean()
        upvote.save()
        return redirect(f'/post/{id}/')

@login_required(login_url='/user/login/', redirect_field_name=None)
def post_downvote_create_view(request, id):
    
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        downvote = Downvote(post=post, user=request.user)
        downvote.full_clean()
        downvote.save()
        return redirect(f'/post/{id}/')

@login_required(login_url='/user/login/', redirect_field_name=None)
def post_comment_upvote_create_view(request, post_id, comment_id):
    
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        upvote = Upvote(comment=comment, user=request.user)
        upvote.full_clean()
        upvote.save()
        return redirect(f'/post/{post_id}/')


@login_required(login_url='/user/login/', redirect_field_name=None)
def post_comment_downvote_create_view(request, post_id, comment_id):
    
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        downvote = Downvote(comment=comment, user=request.user)
        downvote.full_clean()
        downvote.save()
        return redirect(f'/post/{post_id}/')


@login_required(login_url='/user/login/', redirect_field_name=None)
def user_follow_create_view(request, id):
    
    if request.method == 'POST':
        followed = User.objects.get(id=id)
        follow = Follow(follower=request.user, followed=followed)
        follow.full_clean()
        follow.save()
        return redirect(f'/user/{id}/')


@login_required(login_url='/user/login/', redirect_field_name=None)
def user_follow_delete_view(request, id):
    
    if request.method == 'POST':
        followed = User.objects.get(id=id)
        follow = Follow.objects.get(follower=request.user, followed=followed)
        follow.delete()
        return redirect(f'/user/{id}/')
