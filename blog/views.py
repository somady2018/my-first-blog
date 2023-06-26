from pathlib import Path
import urllib
import openai
import logging
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm, PromptForm
from .models import Post

openai.api_key = settings.OPENAI_API_KEY
logger = logging.getLogger(__name__)
image_directory = Path(settings.BASE_DIR, 'blog', 'static', 'images')

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # 사용자가 보낸 HTTP 요청에 관련된 정보

    # post_list.html + posts 라는 쿼리셋 render 템플릿 엔진이 렌더링해서 최종 결과 HTML을 클라로 전달
    return render(request, 'blog/post_list.html', { 'posts': posts })

def post_detail(request, pk):
    # pk = 6
    # 404 Not Found 찾지 못함
    post = get_object_or_404(Post, pk=pk)
    post.image_url = Path('images', f'{post.image_prompt}.png')
    return render(request, 'blog/post_detail.html', { 'post': post })

def post_new(request):
    if request.method == 'POST':
        # DB에 저장하는 동작
        form = PostForm(request.POST)

        if form.is_valid():
            # commit = False
            # commit: form에서 사용자가 입력한 것을 데이터베이스에 저장
            # post Post 클래스 
            post = form.save(commit=False)
            # request.user kimsalt, 로그인을 안 한 상태면 익명사용자
            post.author = request.user
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', { 'form': form })

def post_edit(request, pk):
    # pk에 해당하는 Post가 없으면 404 에러를 반환하는 예외를 던진다
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # post 객체 만들기
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        # instance는 게시글 내용을 폼에 미리 넣어서 사용자들이 편집을 할 수 있게
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def generate_post(request):
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.author = request.user
            completion = openai.Completion.create(
                engine='text-davinci-003',
                prompt=post.prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            post.text = completion.choices[0].text
            post.save()

            image_resp = openai.Image.create(prompt=post.image_prompt, size="512x512")
            image_url = image_resp['data'][0]['url']
            Path.mkdir(image_directory, exist_ok=True)
            image_path = Path(image_directory, f'{post.image_prompt}.png')
            urllib.request.urlretrieve(image_url, image_path)

            return redirect('post_detail', pk=post.pk)
    else:
        form = PromptForm()
        
    return render(request, 'blog/generate_post.html', {'form': form})