from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from post.models import Post, Like, Follower, Comment
from django.contrib import messages
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.models import User

def list_view(request):
    if request.user.is_anonymous:
        messages.warning(request, f"lutfen giris yapiniz..")
        return redirect('login')
    
    user_posts = Post.objects.filter(created_by=request.user)
    following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)
    following_posts = Post.objects.filter(created_by__in=following_users)
    users = User.objects.all()
    posts = (user_posts | following_posts).distinct().order_by('-created_at')
    comment_form = CommentForm()
    
    comments = Comment.objects.filter(post__in=posts)
    context = dict(
        posts = posts,
        comment_form = comment_form,
        comments = comments,
        users = users
    )
    return render(request, "post/list.html", context)


def detail_view(request):
    user_posts = Post.objects.filter(created_by=request.user)
    user_post_count = user_posts.count()
    context = dict(
        user_post_count = user_post_count,
        user_posts = user_posts,
    )
    return render(request, "post/detail.html", context)

def create_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            messages.success(request, f"post başarıyla oluşturuldu.")
            return redirect('post:list')
        else:
            messages.error(request, "Form geçersiz. Lütfen gerekli alanları doldurun.")
    else:
        form = PostForm()
    context = dict(
        form = form
        )
    return render(request, "post/create.html", context)

def like_view(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)
    existing_like = Like.objects.filter(user=request.user, post=post).first()
    
    if existing_like:
        existing_like.delete()
        post.likes -= 1
        post.save()
        
    else:
        like = Like(user=request.user, post=post)
        like.save()
        post.likes += 1
        post.save()
    
    return redirect('post:list')

def social_view(request):
    if request.user.is_anonymous:
        return redirect('login')
    
    users = User.objects.exclude(id=request.user.id)

    for user in users:
        user.is_followed = Follower.objects.filter(follower=request.user, following=user).exists()

    context = {'users': users}
    return render(request, 'post/social.html', context)

def follow_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_to_follow = get_object_or_404(User, id=user_id)

        is_following = Follower.objects.filter(follower=request.user, following=user_to_follow).exists()

        if is_following:
            Follower.objects.filter(follower=request.user, following=user_to_follow).delete()
            messages.success(request, f'Artık {user_to_follow.username} kullanıcısını takip etmiyorsunuz.')
        else:
            Follower.objects.create(follower=request.user, following=user_to_follow)
            messages.success(request, f'{user_to_follow.username} kullanıcısını takip ediyorsunuz.')
    return redirect('post:social')

def comment_add_view(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=True)
            comment.user = request.user
            comment.post = post
            comment.save()

    return redirect('post:list')


def explore_view(request):
    # En çok beğeni alan ilk 10 gönderiyi al
    top_posts = Post.objects.order_by('-likes')[:10]
    context = dict(
        top_posts = top_posts
    )
    return render(request, 'post/explore.html', context)



def post_share_view(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)
    users = User.objects.exclude(username=request.user.username)

    if request.method == 'POST':
        selected_username = request.POST.get('selected_username')

        if selected_username:
            recipient_user = get_object_or_404(User, username=selected_username)
            post.shared_with.add(recipient_user)
            messages.success(request, f'Post başarıyla paylaşıldı: {post.content} - {recipient_user.username}')
            return redirect('post:list') 

    return render(request, 'post/share_post_modal.html', {'post': post})

def shared_posts_view(request):
    shared_posts = Post.objects.filter(shared_with=request.user)
    return render(request, 'post/shared_posts.html', {'shared_posts': shared_posts})


def profile_edit_view(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('post:detail')

    return render(request, 'post/profile_edit.html', {'form': form})