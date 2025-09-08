from django.db import models

# Create your models here.

class Question(models.Model):
    question_title = models.CharField()
    answer = models.CharField()


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)


class Quiz(models.Model):
    title = models.CharField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField()
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
