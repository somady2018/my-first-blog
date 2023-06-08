from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    
    #post_list.html + posts 라는 쿼리셋 을 이용해서 render 라는 템플릿엔진이 랜더링해서 최종결과  html을 보여준다. 
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.publish()
            return redirect('post_detail', pk=post.pk)
            
    else:
        form = PostForm()
    
    return render(request, 'blog/post_new.html', {'form': form})