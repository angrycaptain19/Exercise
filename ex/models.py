from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=50)
    question_text = RichTextUploadingField()
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer_text = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now_add=True)
    isTimeout = models.BooleanField()
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ['-pub_date']
