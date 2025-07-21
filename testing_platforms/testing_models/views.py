from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import Test, Question, SysAnswers
from rest_framework import serializers

class SysAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysAnswers
        fields = ['text', 'is_correct', 'reward']

class QuestionSerializer(serializers.ModelSerializer):
    options = SysAnswersSerializer(many=True, required=False)
    correctAnswer = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'options', 'correctAnswer']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Test
        fields = ['title', 'questions']

class TestCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            test = Test.objects.create(
                title=serializer.validated_data['title'],
                created_by=user
            )
            for q in serializer.validated_data['questions']:
                question = Question.objects.create(
                    test_ID=test,
                    text=q['text'],
                    question_type=q['question_type']
                )
                if q['question_type'] in ['single', 'multiple']:
                    for opt in q.get('options', []):
                        SysAnswers.objects.create(
                            question_ID=question,
                            text=opt['text'],
                            is_correct=opt['is_correct'],
                            reward=1
                        )
                elif q['question_type'] == 'text':
                    SysAnswers.objects.create(
                        question_ID=question,
                        text=q.get('correctAnswer', ''),
                        is_correct=True,
                        reward=1
                    )
            return Response({'status': 'ok', 'test_id': test.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
