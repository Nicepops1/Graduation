from django.urls import path
from .views import TestCreateAPIView, TestListAPIView, TestDetailAPIView, TestSubmitAPIView, UserTestResultsAPIView, CreatedTestResultsAPIView, TestDetailedResultsAPIView

urlpatterns = [
    path('tests/create/', TestCreateAPIView.as_view(), name='test-create'),
    path('tests/', TestListAPIView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestDetailAPIView.as_view(), name='test-detail'),
    path('tests/<int:pk>/detailed-results/', TestDetailedResultsAPIView.as_view(), name='test-detailed-results'),
    path('tests/submit/', TestSubmitAPIView.as_view(), name='test-submit'),
    path('user/tests/results/', UserTestResultsAPIView.as_view(), name='user-test-results'),
    path('user/created-tests/results/', CreatedTestResultsAPIView.as_view(), name='created-test-results'),
]
