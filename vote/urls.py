from django.urls import path

from vote.views import UpVote, DownVote

urlpatterns = [
    path(
        "<int:meetup_id>/questions/<int:question_id>/upvote/",
        UpVote.as_view(),
        name="upvote",
    ),
    path(
        "<int:meetup_id>/questions/<int:question_id>/downvote/",
        DownVote.as_view(),
        name="downvote",
    )
]
