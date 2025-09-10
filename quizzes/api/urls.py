from django.urls import path

from .views import QuizCreateAPIView, QuizListAPIView

urlpatterns = [
    path('createQuiz/', QuizCreateAPIView.as_view(), name='create_quiz'),
    path('quizzes/', QuizListAPIView.as_view(), name='quizzes'),
]
