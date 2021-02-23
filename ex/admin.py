from django.contrib import admin
from .models import Question, Answer


# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'pub_date', 'deadline')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'student', 'pub_date', 'isTimeout')
