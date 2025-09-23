import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quizzes.models import Question, Quiz


class QuestionsListSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'answer', 'question_options', 'created_at', 'updated_at']

    def get_question_options(self, obj):
        return [obj.option1, obj.option2, obj.option3, obj.option4]


class QuestionCreateSerializer(serializers.ModelSerializer):
    question_options = serializers.ListField()
    class Meta:
        model = Question
        fields = ['question_title', 'question_options', 'answer']

    def create(self, validated_data):
        options = validated_data.pop("question_options")
        validated_data["option1"] = options[0]
        validated_data["option2"] = options[1]
        validated_data["option3"] = options[2]
        validated_data["option4"] = options[3]
        return super().create(validated_data)


class QuizListDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz_id=obj.id)
        return QuestionsListSerializer(questions, many=True).data

class QuizCreateSerializer(serializers.ModelSerializer):
    questions_data = QuestionCreateSerializer(many=True, write_only=True)
    questions = QuestionsListSerializer( many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Quiz
        fields = ["user", "video_url", "title", "description", "questions", "questions_data"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions_data")
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            question_serializer = QuestionCreateSerializer(data=question_data)
            question_serializer.is_valid(raise_exception=True)
            question_serializer.save(quiz=quiz)

        return quiz
