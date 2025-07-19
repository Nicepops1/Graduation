from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class Test(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class Question(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     text = models.TextField()
#     question_type = models.CharField(max_length=50)
#     answer = models.CharField(max_length=200)
#     time_for_answer = models.TimeField(max_length=200)

# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=200)
#     is_correct = models.BooleanField(default=False)

# class Result(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     completed_at = models.DateTimeField(auto_now_add=True)