delete_answer_msg = {
    "status": 200,
    "data": [{"success": "Answer deleted deleted", "status": 200}],
}
from django.urls import reverse


def test_anonymous_user_cannot_delete_an_answer(
        api_client, db, answered_question
):
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {
        "detail": "Authentication credentials were not provided.",
        "status": 403,
    }:
        raise AssertionError()


def test_non_Staff_user_cannot_delete_an_answer(
        api_client, db, user1, answered_question
):
    api_client.force_authenticate(user=user1)
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Only staff are allowed to delete answers",
    }:
        raise AssertionError()


def test_Staff_user_cannot_delete_an_answer_with_invalid_answer_id(
        api_client, db, user1, answered_question
):
    api_client.force_authenticate(user=answered_question.created_by)
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": 2,
            },
        )
    )
    if not response.status_code == 404:
        raise AssertionError()

    if not response.data == {"status": 404, "error": "Answer does not exist"}:
        raise AssertionError()


def test_admin_user_can_delete_any_answer(
        api_client, db, admin_user, answered_question
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 200:
        raise AssertionError()

    if not response.data == delete_answer_msg:
        raise AssertionError()


def test_staff_cannot_delete__an_answer_created_by_another_staff_them(
        api_client, db, staff2, answered_question
):
    api_client.force_authenticate(user=staff2)
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "You cannot delete an answer created by another user",
    }:
        raise AssertionError()


def test_staff_can_delete_answer_created_by_them(
        api_client, db, staff1, answered_question
):
    api_client.force_authenticate(user=answered_question.created_by)
    response = api_client.delete(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 200:
        raise AssertionError()

    if not response.data == delete_answer_msg:
        raise AssertionError()
