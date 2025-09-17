import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quizzes.models import Question, Quiz


class QuestionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'option1', 'option2', 'option3', 'option4', 'answer', 'created_at', 'updated_at']

class QuizListSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz_id=obj.id)
        return QuestionsListSerializer(questions, many=True).data

class QuizCreateSerializer(serializers.ModelSerializer):
    questions = serializers.ListField()
    class Meta:
        model = Quiz
        fields = ["video_url", "title", "description", "questions"]

    def create(self, validated_data):
        return super().create(validated_data)
