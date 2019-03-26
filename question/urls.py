from django.urls import path

from question.views import Questions, OneQuestion

urlpatterns = [
    path("<int:meetup_id>/questions/", Questions.as_view(), name="questions"),
    path(
        "<int:meetup_id>/questions/<int:question_id>/",
        OneQuestion.as_view(),
        name="question",
    ),
]
