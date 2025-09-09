from django.urls import path

from .views import QuizListAPIView

urlpatterns = [
    path('quizzes/', QuizListAPIView.as_view(), name='quizzes'),
]
