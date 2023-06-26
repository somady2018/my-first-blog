from django.conf import settings
from django.db import models
from django.utils import timezone

#Post가 Model을 상속받는다. Model:부모클래스, Post:자식클래스 - 즉 MOdel의 속성이나 메서드를 post에서 그대로 쓸 수 있다. 
class Post(models.Model):
    #속성
    #외래키 : 다른 모델을 가리키는 속성. on_delete: author 가 지워졌을 경우 포스트 테이블의 데이터를 어떻게 할 것인가. 
    #CASCADE :  Autuor가 지워지면 post도 지워지게 하겠다. 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #charfield 제목이 200자로 길이가 정해져있는 필드. 
    title = models.CharField(max_length=200)
    #Text 게시글본문. 길이가정해져있지 않은 문자열. 
    text = models.TextField()
    #날짜,시간을 담는 필드. 기본값이 현재시각. 
    created_date = models.DateTimeField(
            default=timezone.now)
    #게시글이 퍼블리시된 저장된시간. 
    published_date = models.DateTimeField(
            blank=True, null=True)
    #0627추가
    prompt = models.CharField(max_length=200, default="Not created by AI")
    image_prompt = models.CharField(max_length=200, default="Not created by AI")

    #게시글을 저장하는 메서드. 
    def publish(self):
        #self 자기자신의 오브젝트를 가리키는 약속. 
        self.published_date = timezone.now()
        #Post가 실제로 데이터베이스에 저장이 된다. 
        self.save()
    #매서드
    #__str__: 언더바 특수메서드들임. 포스트라는 객체를 문자열로 바꿔주는 메서드. 
    def __str__(self):
        return self.title