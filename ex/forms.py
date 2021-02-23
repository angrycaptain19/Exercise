from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Question


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=20, min_length=2,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '请输入题目标题'}), label='题目标题')
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                                     'class': 'form-control'}),
                                   label='截至日期')
    question_text = forms.CharField(widget=CKEditorUploadingWidget(), label='')



class AnswerForm(forms.Form):
    answer_text = forms.CharField(widget=CKEditorUploadingWidget(), label='')
    question_pk = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        # 问题存在验证
        question_pk = self.cleaned_data['question_pk']
        try:
            Question.objects.get(pk=question_pk)
        except Exception as e:
            raise ValidationError('问题不存在')

        return self.cleaned_data
