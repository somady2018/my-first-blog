from django.shortcuts import render
from .forms import PostForm

def post_list(request):
    return render(request, 'blog/post_list.html', {})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
