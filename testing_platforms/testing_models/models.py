from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time_to_complete = models.TimeField(null=True)

class Question(models.Model):
    test_ID = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50)

class SysAnswers(models.Model):
    question_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    reward = models.IntegerField(default=1)

class UserAnswers(models.Model):
    question_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_ID = models.ForeignKey(SysAnswers, on_delete=models.CASCADE, null=True, blank=True)
    waste_time = models.TimeField()
    text = models.CharField(max_length=200, null=True)
    result = models.ForeignKey('Result', on_delete=models.CASCADE, null=True, blank=True)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    wasted_time = models.TimeField(null=True)