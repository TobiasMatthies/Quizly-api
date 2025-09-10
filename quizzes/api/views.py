from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from quizzes.models import Quiz

from .permissions import IsAuthenticatedFromCookie
from .serializers import QuizCreateSerializer, QuizListSerializer


class QuizCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedFromCookie]
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "invalid url"}, status=status.HTTP_400_BAD_REQUEST)

        return Response("ok", status=status.HTTP_200_OK)



class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticatedFromCookie]
