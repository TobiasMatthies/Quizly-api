import requests
import yt_dlp
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response

from core.settings import ydl_opts as ydl_options
from quizzes import utils
from quizzes.models import Quiz
from quizzes.utils import (audio_download_hook, generate_quiz,
                           generate_transcribtion)

from .permissions import IsAuthenticatedFromCookie, IsQuizOwner
from .serializers import QuizCreateSerializer, QuizListDetailSerializer


class QuizCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedFromCookie]
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer

    def post(self, request):
        url = request.data["url"]
        try:
            response = requests.head(url)

        except Exception as e:
            raise ValidationError(e)

        ydl_options["progress_hooks"] = [audio_download_hook]

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            error_code = ydl.download(url)

        if utils.filename:
            transcribtion = generate_transcribtion()
            quiz_data = generate_quiz(transcribtion, url)

            serializer = self.get_serializer(data=quiz_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("message: could not generate quiz from video", status=status.HTTP_400_BAD_REQUEST)



class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListDetailSerializer
    permission_classes = [IsAuthenticatedFromCookie]


class QuizRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListDetailSerializer
    permission_classes = [IsQuizOwner]

    def get_object(self):
        quiz = Quiz.objects.get(id=self.kwargs["id"])
        self.check_object_permissions(self.request, quiz)
        return quiz
