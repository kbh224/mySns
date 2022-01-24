# tweet/models.py
from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager #태그추가



# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"
#foreignkey 다른 모델에서 가져오겠다
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True) #빈간이어도 작동
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)