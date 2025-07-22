from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import Test, Question, SysAnswers, UserAnswers, Result
from rest_framework import serializers

class TestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title']

class SysAnswersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SysAnswers
        fields = ['id', 'text', 'is_correct', 'reward']

class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    options = SysAnswersSerializer(many=True, source='sysanswers_set', required=False)
    correctAnswer = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'options', 'correctAnswer']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set', read_only=True)
    class Meta:
        model = Test
        fields = ['title', 'questions']

class TestCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    questions = serializers.ListField()

class TestCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TestCreateSerializer(data=request.data)
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

class TestListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        tests = Test.objects.all()
        serializer = TestListSerializer(tests, many=True)
        return Response(serializer.data)

class UserTestResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        results = Result.objects.filter(user=user)
        data = [
            {
                'id': r.id,
                'test_name': r.test.title,
                'score': r.score,
                'completed_at': r.completed_at,
                'wasted_time': r.wasted_time
            }
            for r in results
        ]
        return Response(data)

class CreatedTestResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        results = Result.objects.filter(test__created_by=user)
        data = [
            {
                'id': r.id,
                'username': r.user.username,
                'test_id': r.test.id,
                'test_name': r.test.title,
                'score': r.score,
                'completed_at': r.completed_at,
                'wasted_time': r.wasted_time
            }
            for r in results
        ]
        return Response(data)

class TestSubmitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        test_id = data.get('test_id')
        answers = data.get('answers', [])
        score = 0
        from .models import Test, Result
        test = Test.objects.get(id=test_id)
        # Сначала создаём запись о результате теста (чтобы получить id)
        result_obj = Result.objects.create(
            user=user,
            test=test,
            score=0,  # временно, обновим после подсчёта
            wasted_time=None
        )
        for ans in answers:
            question_id = ans.get('question_id')
            answer_ids = ans.get('answer_ids', [])
            text = ans.get('text', None)
            question = Question.objects.get(id=question_id)
            if answer_ids:
                correct_ids = set(SysAnswers.objects.filter(question_ID=question, is_correct=True).values_list('id', flat=True))
                user_ids = set(answer_ids)
                if user_ids == correct_ids:
                    score += sum(SysAnswers.objects.filter(id__in=correct_ids).values_list('reward', flat=True))
                for aid in answer_ids:
                    UserAnswers.objects.create(
                        question_ID_id=question_id,
                        user_ID=user,
                        answer_ID_id=aid,
                        waste_time='00:00:00',
                        text=None,
                        result=result_obj
                    )
            elif text is not None:
                correct_answer = SysAnswers.objects.filter(question_ID=question, is_correct=True).first()
                if correct_answer and correct_answer.text.strip().lower() == (text or '').strip().lower():
                    score += correct_answer.reward
                UserAnswers.objects.create(
                    question_ID_id=question_id,
                    user_ID=user,
                    answer_ID=None,
                    waste_time='00:00:00',
                    text=text,
                    result=result_obj
                )
        # Обновляем score в Result
        result_obj.score = score
        result_obj.save()
        return Response({'status': 'ok'}, status=201)

class TestDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            test = Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TestSerializer(test)
        return Response(serializer.data)

class TestDetailedResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        try:
            test = Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found'}, status=404)
        if test.created_by != user:
            return Response({'error': 'Forbidden'}, status=403)
        questions = list(Question.objects.filter(test_ID=test))
        question_map = {q.id: q.text for q in questions}
        correct_map = {}
        for q in questions:
            correct_map[q.id] = set(SysAnswers.objects.filter(question_ID=q, is_correct=True).values_list('id', flat=True))
        # Собираем результаты по пользователям
        results = Result.objects.filter(test=test).order_by('completed_at')
        data = []
        for res in results:
            u = res.user
            user_result = {'username': u.username, 'answers': [], 'score': res.score, 'completed_at': res.completed_at}
            for q in questions:
                user_ans = UserAnswers.objects.filter(user_ID=u, question_ID=q, result=res)
                if q.question_type in ['single', 'multiple']:
                    user_ans_ids = set(user_ans.values_list('answer_ID', flat=True))
                    is_correct = user_ans_ids == correct_map[q.id]
                else:
                    correct_text = SysAnswers.objects.filter(question_ID=q, is_correct=True).first()
                    user_text = user_ans.first().text if user_ans.exists() else ''
                    is_correct = correct_text and user_text and correct_text.text.strip().lower() == user_text.strip().lower()
                user_result['answers'].append({
                    'question': q.text,
                    'is_correct': is_correct,
                    'user_answer': user_ans.first().text if q.question_type == 'text' and user_ans.exists() else None
                })
            data.append(user_result)
        return Response({'questions': [q.text for q in questions], 'results': data})
