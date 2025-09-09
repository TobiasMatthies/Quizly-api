from rest_framework.generics import ListAPIView

from quizzes.models import Quiz

from .permissions import IsAuthenticatedFromCookie
from .serializers import QuizListSerializer


# Create your views here.
class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticatedFromCookie]
