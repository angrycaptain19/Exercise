from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:pk>', views.question_detail, name='question_detail'),
    path('update_answer', views.update_answer, name='update_answer'),
    path('answer/', views.answer_list, name='answer_list'),
    path('answer/<int:pk>', views.answer_detail, name='answer_detail'),
    path('question_upload', views.question_upload, name='question_upload'),
]
