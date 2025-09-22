from django.urls import path

from .views import (QuizCreateAPIView, QuizListAPIView,
                    QuizRetrieveUpdateDestroyAPIView)

urlpatterns = [
    path('createQuiz/', QuizCreateAPIView.as_view(), name='create_quiz'),
    path('quizzes/', QuizListAPIView.as_view(), name='quizzes'),
    path('quizzes/<int:id>/', QuizRetrieveUpdateDestroyAPIView.as_view(), name='quiz-detail'),
]
