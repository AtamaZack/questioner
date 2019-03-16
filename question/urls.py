from django.urls import path

from question.views import Questions, OneQuestion, UpVote, DownVote, CommentList, CommentDetail

urlpatterns = [
    path("<int:meetup_id>/questions/", Questions.as_view(), name="questions"),
    path(
        "<int:meetup_id>/questions/<int:question_id>/",
        OneQuestion.as_view(),
        name="question",
    ),
    path(
        "<int:meetup_id>/questions/<int:question_id>/upvote/",
        UpVote.as_view(),
        name="upvote",
    ),
    path(
        "<int:meetup_id>/questions/<int:question_id>/downvote/",
        DownVote.as_view(),
        name="downvote",
    ),
    path("<int:meetup_id>/questions/<question_id>/comments",
         CommentList.as_view(), name='comment'),
    path("<int:meetup_id>/questions/<question_id>/comments/<int:pk>",
         CommentDetail.as_view(), name='comment_detail')
]
