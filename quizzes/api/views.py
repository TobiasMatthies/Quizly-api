import json

import requests
import whisper
import yt_dlp
from google import genai
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from core.settings import ydl_opts as ydl_options
from quizzes import utils
from quizzes.models import Quiz

from .permissions import IsAuthenticatedFromCookie
from .serializers import QuizCreateSerializer, QuizListSerializer

client = genai.Client()


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

        ydl_options["progress_hooks"] = [utils.audio_download_hook]

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            error_code = ydl.download(url)

        if utils.filename:
            model = whisper.load_model("turbo")
            transcribtion = model.transcribe(utils.filename)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    json.dumps(transcribtion), json.dumps(utils.prompt)
                ],
                config={
                    "response_mime_type": "application/json"
                }
            )

            json_string = response.candidates[0].content.parts[0].text
            quiz_data = json.loads(json_string)
            quiz_data["video_url"] = url

            serializer = self.get_serializer(data=quiz_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("message: could not generate quiz from video", status=status.HTTP_400_BAD_REQUEST)



class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticatedFromCookie]
