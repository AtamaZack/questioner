from django.urls import path

from answer.views import CreateReadAnswers, EditDeleteAnswers

urlpatterns = [
    path(
        "<int:meetup_id>/questions/<int:question_id>/answers/",
        CreateReadAnswers.as_view(),
        name="create_read_answers",
    ),
    path(
        "<int:meetup_id>/questions/<int:question_id>/answers/<int:answer_id>/",
        EditDeleteAnswers.as_view(),
        name="edit_delete_answers",
    ),
]
# format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)
